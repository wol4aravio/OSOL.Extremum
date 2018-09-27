from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import torch


def piecewise_variance_measure(switch_points, controls, Lp, pytorch=False):
    nu = 0.0
    for i in range(len(switch_points) - 1):
        tau = switch_points[i + 1] - switch_points[i]
        delta = controls[i + 1] - controls[i]
        if not pytorch:
            nu += np.power(np.abs(delta / tau), Lp)
        else:
            nu += torch.pow(torch.abs(delta / tau), Lp)
    return nu


class PiecewiseConstantController:

    def __init__(self, control_name, switch_points, controls, penalty=0.0, variance_power=1):
        self.control_name = control_name
        self.switch_points = switch_points
        self.controls = controls
        self.penalty = penalty
        self.variance_power = variance_power

    def set_parameters(self, parameters):
        param_names = ['{0}_{1}'.format(self.control_name, i) for i in range(len(self.switch_points))]
        self.controls = list(map(lambda n: parameters[n], param_names))
        return

    def get_control(self, t, x):
        timed_control = list(zip(self.switch_points, self.controls))
        control = [c for (tau, c) in timed_control if tau <= t][-1]
        return self.control_name, control

    def get_measure_variance(self, t, x, pytorch=False):
        return piecewise_variance_measure(self.switch_points, self.controls, self.variance_power, pytorch)


class PiecewiseLinearController:

    def __init__(self, control_name, switch_points, controls, penalty=0.0, variance_power=1):
        self.control_name = control_name
        self.switch_points = switch_points
        self.controls = controls
        self.penalty = penalty
        self.variance_power = variance_power

    def set_parameters(self, parameters):
        param_names = ['{0}_{1}'.format(self.control_name, i) for i in range(len(self.switch_points))]
        self.controls = list(map(lambda n: parameters[n], param_names))
        return

    def get_control(self, t, x):
        time_intervals = list(zip(self.switch_points[:-1], self.switch_points[1:]))
        control_pairs = list(zip(self.controls[:-1], self.controls[1:]))
        control_intervals = list(zip(time_intervals, control_pairs))
        if t <= self.switch_points[-1]:
            ((t1, t2), (c1, c2)) = next(((t1, t2), c) for ((t1, t2), c) in control_intervals if t1 <= t <= t2)
            control = ((t2 - t) * c1 + (t - t1) * c2) / (t2 - t1)
        else:
            control = self.controls[-1]
        return self.control_name, control

    def get_measure_variance(self, t, x, pytorch=False):
        return piecewise_variance_measure(self.switch_points, self.controls, self.variance_power, pytorch)


class ExplicitController:

    def __init__(self, control_name, formula, vars, param_names, penalty=0.0, variance_power=1):
        self.control_name = control_name
        sym_vars = list(map(symbols, vars + param_names))
        self.vars = vars
        self.param_names = param_names
        self.generated_controls = []
        self.parameters = None
        self._f = lambdify(sym_vars, parse_expr(formula), np)
        self.penalty = penalty
        self.variance_power = variance_power

    def set_parameters(self, parameters):
        self.generated_controls = []
        self.parameters = list(map(lambda n: parameters[n], self.param_names))
        return

    def get_control(self, t, x):
        args = []
        for v in self.vars:
            if v == 't':
                args.append(t)
            elif v in x:
                args.append(x[v])
            else:
                raise Exception("Smth wrong with formulas")
        control = self._f(*(args + self.parameters))
        self.generated_controls.append(control)
        return self.control_name, control

    def get_measure_variance(self, t, x, pytorch=False):
        return piecewise_variance_measure(t[:-1], self.generated_controls, self.variance_power, pytorch)


def create_controller_from_dict(data):
    penalty = data.get('penalty', 0.0)
    variance_power = data.get('variance_power', 1.0)

    if data['type'] == 'piecewise_constant':
        switch_points = data['switch_points']
        if 'controls' in data:
            controls = data['controls']
        else:
            controls = None
        return PiecewiseConstantController(data['name'], switch_points, controls, penalty, variance_power)
    elif data['type'] == 'piecewise_linear':
        switch_points = data['switch_points']
        if 'controls' in data:
            controls = data['controls']
        else:
            controls = None
        return PiecewiseLinearController(data['name'], switch_points, controls, penalty, variance_power)
    elif data['type'] == 'explicit':
        return ExplicitController(data['name'], data['formula'], data['vars'], data['param_names'], penalty, variance_power)
    else:
        raise Exception('Unsupported Controller')


def convert(controller, **params):
    target_dict = {}
    target_dict['penalty'] = params.get('penalty', 0.0)
    target_dict['variance_power'] = params.get('variance_power', 1.0)
    if 'type' not in params:
        raise Exception('No type is provided')
    else:
        target_dict['type'] = params.get('type')
        if target_dict['type'] == 'explicit':
            raise Exception('Currently conversion to explicit controller is not supported')
        elif target_dict['type'] == 'piecewise_linear' or target_dict['type'] == 'piecewise_constant':
            target_dict['switch_points'] = params.get('switch_points')
            target_dict['controls'] = []
            for t in target_dict['switch_points']:
                target_dict['controls'].append(controller.get_control(t, x=None))
        else:
            raise Exception('Unknown target type {}'.format(target_dict['type']))
        return create_controller_from_dict(target_dict)
