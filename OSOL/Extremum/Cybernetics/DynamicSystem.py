from OSOL.Extremum.Numerical_Objects.Interval import Interval
from OSOL.Extremum.Cybernetics.Controllers import create_controller_from_dict

from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import torch


class DynamicSystem:

    def __init__(self,
                 sampling_type, sampling_eps, sampling_max_steps,
                 f, state_vars, initial_conditions,
                 controllers, control_vars, control_bounds,
                 aux, etc_vars,
                 integral_criteria, terminal_criterion,
                 terminal_constraints, phase_constraints,
                 pytorch=False):

        self._state_vars = state_vars + ['I_integral_{}'.format(i + 1)
                                         for i in range(len(integral_criteria))] + ['phase_{}'.format(i + 1)
                                                                                    for i in range(len(phase_constraints))]
        self._control_vars = control_vars
        self._etc_vars = etc_vars
        self._vars_str = ['t'] + self._state_vars + self._control_vars + self._etc_vars
        self._sym_vars = list(map(symbols, self._vars_str))
        self._is_pytorch = pytorch

        if not pytorch:
            libs = _np_lib
            self._init_sim = _init_dummy
            self._error_measurer = _measure_error
            self._terminal_error_measurer = _terminal_error_dummy
            self._control_constrainer = _constrain_control_dummy
        else:
            libs = _torch_lib
            self._init_sim = _init_pytorch
            self._error_measurer = _measure_error_tensor
            self._terminal_error_measurer = _terminal_error_pytorch
            self._control_constrainer = _constrain_control_pytorch

        self._integral_criteria = [lambdify(self._sym_vars, parse_expr(c), libs['dummy']) for c in integral_criteria]
        self._terminal_criterion = lambdify(self._sym_vars[:(1 + len(self._state_vars))],
                                            parse_expr(terminal_criterion), libs['dummy'])

        self._initial_conditions = initial_conditions

        self._controllers = controllers
        self._control_bounds = control_bounds

        self._f = f
        for v in self._state_vars:
            if not v.startswith('I_integral_') and not v.startswith('phase_'):
                self._f[v] = lambdify(self._sym_vars, parse_expr(self._f[v]), libs['dummy'])
        for i in range(len(integral_criteria)):
            self._f['I_integral_{}'.format(i + 1)] = self._integral_criteria[i]
            self._initial_conditions['I_integral_{}'.format(i + 1)] = 0.0

        self._phase_constraints = phase_constraints
        for i in range(len(self._phase_constraints)):
            lib_id = self._phase_constraints[i]['penalty'][1]
            self._f['phase_{}'.format(i + 1)] = lambdify(
                self._sym_vars,
                parse_expr('phase({0}, {1}, {2})'.format(
                    self._phase_constraints[i]['equation'],
                    self._phase_constraints[i]['penalty'][0],
                    float(self._phase_constraints[i]['norm'][1:]))), libs[lib_id])
            self._initial_conditions['phase_{}'.format(i + 1)] = 0.0

        self._aux = aux
        counter = 0
        for v in self._etc_vars:
            self._aux[v] = lambdify(self._sym_vars[:(len(self._sym_vars) - (len(self._etc_vars) - counter))],
                                    parse_expr(self._aux[v]), libs['dummy'])
            counter += 1

        self._sampling_type = sampling_type
        self._sampling_eps = sampling_eps
        self._sampling_max_steps = sampling_max_steps
        if sampling_type == 'Euler':
            self._prolong = self.prolong_Euler
        elif sampling_type == 'RK4':
            self._prolong = self.prolong_RK4
        else:
            raise Exception('Unknown sampling_type: {}'.format(sampling_type))

        self._terminal_constraints = terminal_constraints
        for i in range(len(self._terminal_constraints)):
            self._terminal_constraints[i]['equation'] = lambdify(self._sym_vars[:(len(self._sym_vars) - len(self._etc_vars) - len(self._control_vars))],
                                                                 parse_expr(self._terminal_constraints[i]['equation']), libs['dummy'])        

    @classmethod
    def from_dict(cls, data, pytorch=False):

        sampling_type = data['sampling_type']
        sampling_eps = data['sampling_eps']
        sampling_max_steps = data['sampling_max_steps']

        state_vars = [d['component'] for d in data['ode']]
        control_vars = [d['name'] for d in data['controllers']]
        etc_vars = [d['component'] for d in data['auxiliary']]
        f = {d['component']: d['equation'] for d in data['ode']}
        initial_conditions = {d['name']: d['value'] for d in data['initial_conditions']}
        controllers = {d['name']: create_controller_from_dict(d) for d in data['controllers']}
        control_bounds = {d['name']: (d['min'], d['max']) for d in data['control_bounds']}
        aux = {d['component']: d['equation'] for d in data['auxiliary']}

        integral_criterion = data['efficiency']['integral']
        terminal_criterion = data['efficiency']['terminal']

        terminal_constraints = []
        for d in data['constraints']['terminal']:
            constraint = {
                'equation': d['equation'],
                'max_error': d['max_error'],
                'penalty': d['penalty'],
                'norm': d['norm']
            }
            terminal_constraints.append(constraint)

        phase_constraints = []
        for d in data['constraints']['phase']:
            constraint = {
                'equation': d['equation'],
                'penalty': d['penalty'],
                'norm': d['norm']
            }
            phase_constraints.append(constraint)

        return cls(sampling_type, sampling_eps, sampling_max_steps,
                   f, state_vars, initial_conditions,
                   controllers, control_vars, control_bounds,
                   aux, etc_vars,
                   integral_criterion, terminal_criterion,
                   terminal_constraints, phase_constraints, pytorch=pytorch)

    def get_aux(self, t, x, u):
        values = [t] + list(x.values()) + list(u.values())
        aux = {}
        for name, eq in self._aux.items():
            aux[name] = eq(*(values + list(aux.values())))
        return aux

    def prolong_Euler(self, t, x, u, a, eps):
        values = [t] + list(x.values()) + list(u.values()) + list(a.values())
        new_state = {
            v: x[v] + eq(*values) * eps 
            for v, eq in self._f.items()}
        return new_state

    def prolong_RK4(self, t, x, u, a, eps):

        def _helper(ds, values):
            return {v: eq(*values) for v, eq in ds._f.items()}

        values = [t] + list(x.values()) + list(u.values()) + list(a.values())
        k1 = _helper(self, values)

        x_new = dict([(v, x[v] + 0.5 * eps * k1[v]) for v in self._state_vars])
        a_new = self.get_aux(t + 0.5 * eps, x_new, u)
        values = [t + 0.5 * eps] + list(x_new.values()) + list(u.values()) + list(a_new.values())
        k2 = _helper(self, values)

        x_new = dict([(v, x[v] + 0.5 * eps * k2[v]) for v in self._state_vars])
        a_new = self.get_aux(t + 0.5 * eps, x_new, u)
        values = [t + 0.5 * eps] + list(x_new.values()) + list(u.values()) + list(a_new.values())
        k3 = _helper(self, values)

        x_new = dict([(v, x[v] + eps * k3[v]) for v in self._state_vars])
        a_new = self.get_aux(t + eps, x_new, u)
        values = [t + eps] + list(x_new.values()) + list(u.values()) + list(a_new.values())
        k4 = _helper(self, values)

        x_new = dict([(v, x[v] + (k1[v] + 2.0 * k2[v] + 2.0 * k3[v] + k4[v]) * (eps / 6.0)) for v in self._state_vars])

        return x_new
    
    def simulate(self, params):
        for v in self._control_vars:
            self._controllers[v].set_parameters(params)
        eps = self._sampling_eps
        max_steps = self._sampling_max_steps
        times, states = self._init_sim(self, params)

        controls = []
        errors_terminal_state = 0.0
        for _ in range(1, max_steps + 1):
            t = times[-1]
            x = states[-1]
            u = dict([self._controllers[v].get_control(t, x) for v in self._control_vars])
            u = self._control_constrainer(self, u)
            a = self.get_aux(t, x, u)
            x_next = self._prolong(t, x, u, a, eps)
            times.append(t + eps)
            states.append(x_next)
            controls.append(u)
            if len(self._terminal_constraints) != 0:
                errors_terminal_state = []
                stop = True
                for constraint in self._terminal_constraints:
                    eq = constraint['equation']
                    max_error = constraint['max_error']
                    [penalty, penalty_type] = constraint['penalty']
                    norm = constraint['norm']

                    values = [times[-1]] + list(x_next.values())

                    error = self._error_measurer(eq(*values))
                    if error > max_error:
                        stop = False
                    errors_terminal_state.append(self._terminal_error_measurer(penalty_type, error, penalty, norm))

                if stop:
                    break
        I_integral = [states[-1]['I_integral_{}'.format(i + 1)] for i in range(len(self._integral_criteria))]
        I_terminal = self._terminal_criterion(*([times[-1]] + list(states[-1].values())))
        if isinstance(I_terminal, np.ndarray):
            I_terminal = I_terminal.tolist()
        phase_errors = [states[-1]['phase_{}'.format(i + 1)] for i in range(len(self._phase_constraints))]
        states = [{k: v for (k, v) in s.items() if not k.startswith('I_integral_') and not k.startswith('phase_')} for s in states]
        controller_variance = []
        for c in self._controllers.values():
            if c.penalty == 0.0:
                controller_variance.append(0.0)
            else:
                controller_variance.append(c.penalty * c.get_measure_variance(times, states, self._is_pytorch))
        return times, states, controls, I_integral, I_terminal, errors_terminal_state, phase_errors, controller_variance


def _phase_explicit(x, penalty, norm):
    if isinstance(x, Interval):
        return Interval(_phase_explicit(x.left, penalty, norm), _phase_explicit(x.right, penalty, norm))
    else:
        return np.power(penalty * max(x, 0.0), norm)


def _phase_explicit_pytorch(x, penalty, norm):
    return (penalty * x(min=0.0, max=None)) ** norm


def _phase_implicit(x, penalty, norm):
    if isinstance(x, Interval):
        return Interval(_phase_implicit(x.left, penalty, norm), _phase_implicit(x.right, penalty, norm))
    else:
        return penalty * np.power(max(x, 0.0), norm)


def _phase_implicit_pytorch(x, penalty, norm):
    return penalty * (x.clamp(min=0.0, max=None) ** norm)


def _init_dummy(ds, params):
    times = [0.0]
    states = [dict([(v, ds._initial_conditions[v]) for v in ds._state_vars])]
    return times, states

def _init_pytorch(ds, params):
    times = [torch.tensor([0.0], dtype=torch.float32, requires_grad=True)]
    states = [dict([(v, torch.tensor([self._initial_conditions[v]], dtype=torch.float32, requires_grad=True))
                for v in self._state_vars])]
    return times, states


def _measure_error(v):
    if isinstance(v, Interval):
        return v.abs().left
    else:
        return np.abs(v)


def _measure_error_tensor(v):
    return torch.abs(v)


def _constrain(v, min_max):
    if isinstance(v, Interval):
        return Interval(_constrain(v.left, min_max), _constrain(v.right, min_max))
    else:
        return np.clip(v, min_max[0], min_max[1])


def _constrain_tensor(v, min_max):
    return v.clamp(min=min_max[0], max=min_max[1])


def _terminal_error_dummy(penalty_type, error, penalty, norm):
    if penalty_type == "explicit":
        return np.power(penalty * error, float(norm[1:]))
    else:
        return penalty * np.power(error, float(norm[1:]))


def _terminal_error_pytorch(penalty_type, error, penalty, norm):
    if penalty_type == "explicit":
        return torch.pow(penalty * error, float(norm[1:]))
    else:
        return penalty * torch.pow(error, float(norm[1:]))


def _constrain_control_dummy(ds, u):
    u_constrained = {v: _constrain(u[v], ds._control_bounds[v]) for v in ds._control_vars}
    return u_constrained


def _constrain_control_pytorch(ds, u):
    u_constrained = {}
    for v in ds._control_vars:
        u_constrained[v] = _constrain_tensor(u[v], ds._control_bounds[v])
        u_constrained[v].retain_grad()
    return u_constrained


_np_lib = {
    'dummy': [np],
    'explicit': [np, {'phase': _phase_explicit}],
    'implicit': [np, {'phase': _phase_implicit}]
    }


_torch_lib = {
    'dummy': [torch],
    'explicit': [torch, {'phase': _phase_explicit_pytorch}],
    'implicit': [torch, {'phase': _phase_implicit_pytorch}]
    }
