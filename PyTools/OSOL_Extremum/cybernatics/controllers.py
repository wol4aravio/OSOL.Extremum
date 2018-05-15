from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np


class PiecewiseConstantController:

    def __init__(self, control_name, switch_points, controls):
        self.control_name = control_name
        self.switch_points = switch_points
        self.controls = controls

    def set_parameters(self, parameters):
        param_names = ['{0}_{1}'.format(self.control_name, i) for i in range(len(self.switch_points))]
        self.controls = list(map(lambda n: parameters[n], param_names))
        return

    def get_control(self, t, x):
        timed_control = list(zip(self.switch_points, self.controls))
        control = [c for (tau, c) in timed_control if tau <= t][-1]
        return self.control_name, control


class PiecewiseLinearController:

    def __init__(self, control_name, switch_points, controls):
        self.control_name = control_name
        self.switch_points = switch_points
        self.controls = controls

    def set_parameters(self, parameters):
        param_names = ['{0}_{1}'.format(self.control_name, i) for i in range(len(self.switch_points))]
        self.controls = list(map(lambda n: parameters[n], param_names))
        return

    def get_control(self, t, x):
        time_intervals = list(zip(self.switch_points[:-1], self.switch_points[1:]))
        control_pairs = list(zip(self.controls[:-1], self.controls[1:]))
        control_intervals = list(zip(time_intervals, control_pairs))
        ((t1, t2), (c1, c2)) = next(((t1, t2), c) for ((t1, t2), c) in control_intervals if t1 <= t <= t2)
        control = ((t2 - t) * c1 + (t - t1) * c2) / (t2 - t1)
        return self.control_name, control


class ExplicitController:

    def __init__(self, control_name, formula, vars, param_names):
        self.control_name = control_name
        sym_vars = list(map(symbols, vars + param_names))
        self.vars = vars
        self.param_names = param_names
        self.parameters = None
        self._f = lambdify(sym_vars, parse_expr(formula), np)

    def set_parameters(self, parameters):
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
        return self.control_name, control


def create_controller_from_dict(data):
    if data['type'] == 'piecewise_constant':
        switch_points = data['switch_points']
        if 'controls' in data:
            controls = data['controls']
        else:
            controls = None
        return PiecewiseConstantController(data['name'], switch_points, controls)
    elif data['type'] == 'piecewise_linear':
        switch_points = data['switch_points']
        if 'controls' in data:
            controls = data['controls']
        else:
            controls = None
        return PiecewiseLinearController(data['name'], switch_points, controls)
    elif data['type'] == 'explicit':
        return ExplicitController(data['control_name'], data['formula'], data['vars'], data['param_names'])
    else:
        raise Exception('Unsupported Controller')

