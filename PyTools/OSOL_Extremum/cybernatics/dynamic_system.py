from OSOL_Extremum.arithmetics.interval import *
from OSOL_Extremum.cybernatics.controllers import create_controller_from_dict

from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np


def phase(x, penalty, norm):
    if isinstance(x, Interval):
        return Interval(phase(x.lower_bound, penalty, norm), phase(x.upper_bound, penalty, norm))
    else:
        return np.power(penalty * max(x, 0.0), norm)


class DynamicSystem:

    def __init__(self,
                 sampling_type, sampling_eps, sampling_max_steps,
                 f, state_vars, initial_conditions,
                 controllers, control_vars, control_bounds,
                 aux, etc_vars,
                 integral_criteria, terminal_criterion,
                 terminal_constraints, phase_constraints):

        self.state_vars = state_vars + ['I_integral_{}'.format(i + 1) for i in range(len(integral_criteria))] + ['phase_{}'.format(i + 1) for i in range(len(phase_constraints))]
        self.control_vars = control_vars
        self.etc_vars = etc_vars
        self.vars_str = ['t'] + self.state_vars + self.control_vars + self.etc_vars
        self.sym_vars = list(map(symbols, self.vars_str))

        self.integral_criteria = [lambdify(self.sym_vars, parse_expr(c), np) for c in integral_criteria]
        self.terminal_criterion = lambdify(self.sym_vars[:(1 + len(self.state_vars))], parse_expr(terminal_criterion), np)

        self.initial_conditions = initial_conditions

        self.controllers = controllers
        self.control_bounds = control_bounds

        self.f = f
        for v in self.state_vars:
            if not v.startswith('I_integral_') and not v.startswith('phase_'):
                self.f[v] = lambdify(self.sym_vars, parse_expr(self.f[v]), np)
        for i in range(len(integral_criteria)):
            self.f['I_integral_{}'.format(i + 1)] = self.integral_criteria[i]
            self.initial_conditions['I_integral_{}'.format(i + 1)] = 0.0

        self.phase_constraints = phase_constraints
        for i in range(len(self.phase_constraints)):
            self.f['phase_{}'.format(i + 1)] = lambdify(self.sym_vars, parse_expr('phase({0}, {1}, {2})'.format(self.phase_constraints[i]['equation'], self.phase_constraints[i]['penalty'], float(self.phase_constraints[i]['norm'][1:]))), [np, {'phase': phase}])
            self.initial_conditions['phase_{}'.format(i + 1)] = 0.0

        self.aux = aux
        counter = 0
        for v in self.etc_vars:
            self.aux[v] = lambdify(self.sym_vars[:(len(self.sym_vars) - (len(self.etc_vars) - counter))], parse_expr(self.aux[v]), np)
            counter += 1

        self.sampling_type = sampling_type
        self.sampling_eps = sampling_eps
        self.sampling_max_steps = sampling_max_steps
        if sampling_type == 'Euler':
            self.prolong = self.prolong_Euler
        elif sampling_type == 'RK4':
            self.prolong = self.prolong_RK4
        else:
            raise Exception('Unknown sampling_type: {}'.format(sampling_type))

        self.terminal_constraints = terminal_constraints
        for i in range(len(self.terminal_constraints)):
            self.terminal_constraints[i]['equation'] = lambdify(self.sym_vars[:(len(self.sym_vars) - len(self.etc_vars) - len(self.control_vars))], parse_expr(self.terminal_constraints[i]['equation']), np)


    @staticmethod
    def measure_error(v):
        if isinstance(v, Interval):
            return v.abs().lower_bound #.upper_bound
        else:
            return np.abs(v)

    @staticmethod
    def constrain(v, min_max):
        if isinstance(v, Interval):
            return Interval(DynamicSystem.constrain(v.lower_bound, min_max),
                            DynamicSystem.constrain(v.upper_bound, min_max))
        else:
            return np.clip(v, min_max[0], min_max[1])


    @classmethod
    def from_dict(cls, data):

        sampling_type = data['sampling_type']
        sampling_eps = data['sampling_eps']
        sampling_max_steps = data['sampling_max_steps']

        state_vars = []
        for d in data['ode']:
            state_vars.append(d['component'])

        control_vars = []
        for d in data['controllers']:
            control_vars.append(d['name'])

        etc_vars = []
        for d in data['auxiliary']:
            etc_vars.append(d['component'])

        f = dict()
        for d in data['ode']:
            f[d['component']] = d['equation']

        initial_conditions = dict()
        for d in data['initial_conditions']:
            initial_conditions[d['name']] = d['value']

        controllers = dict()
        for d in data['controllers']:
            controllers[d['name']] = create_controller_from_dict(d)

        control_bounds = dict()
        for d in data['control_bounds']:
            control_bounds[d['name']] = (d['min'], d['max'])

        aux = dict()
        for d in data['auxiliary']:
            aux[d['component']] = d['equation']

        integral_criterion = data['efficiency']['integral']
        terminal_criterion = data['efficiency']['terminal']

        terminal_constraints = []
        for d in data['constraints']['terminal']:
            constraint = dict()
            constraint['equation'] = d['equation']
            constraint['max_error'] = d['max_error']
            constraint['penalty'] = d['penalty']
            constraint['norm'] = d['norm']
            terminal_constraints.append(constraint)

        phase_constraints = []
        for d in data['constraints']['phase']:
            constraint = dict()
            constraint['equation'] = d['equation']
            constraint['penalty'] = d['penalty']
            constraint['norm'] = d['norm']
            phase_constraints.append(constraint)

        return cls(sampling_type, sampling_eps, sampling_max_steps,
                   f, state_vars, initial_conditions,
                   controllers, control_vars, control_bounds,
                   aux, etc_vars,
                   integral_criterion, terminal_criterion,
                   terminal_constraints, phase_constraints)

    def get_aux(self, t, x, u):
        values = [t] + list(x.values()) + list(u.values())
        aux = {}
        for name, eq in self.aux.items():
            _a = eq(*(values + list(aux.values())))
            aux[name] = _a
        return aux

    def prolong_Euler(self, t, x, u, a, eps):
        values = [t] + list(x.values()) + list(u.values()) + list(a.values())
        new_state = {}
        for v, eq in self.f.items():
            new_state[v] = x[v] + eq(*values) * eps
        return new_state

    def prolong_RK4(self, t, x, u, a, eps):
        values = [t] + list(x.values()) + list(u.values()) + list(a.values())
        k1 = {}
        for v, eq in self.f.items():
            k1[v] = eq(*values)

        x_new = dict([(v, x[v] + 0.5 * eps * k1[v]) for v in self.state_vars])
        a_new = self.get_aux(t + 0.5 * eps, x_new, u)
        values = [t + 0.5 * eps] + list(x_new.values()) + list(u.values()) + list(a_new.values())
        k2 = {}
        for v, eq in self.f.items():
            k2[v] = eq(*values)

        x_new = dict([(v, x[v] + 0.5 * eps * k2[v]) for v in self.state_vars])
        a_new = self.get_aux(t + 0.5 * eps, x_new, u)
        values = [t + 0.5 * eps] + list(x_new.values()) + list(u.values()) + list(a_new.values())
        k3 = {}
        for v, eq in self.f.items():
            k3[v] = eq(*values)

        x_new = dict([(v, x[v] + eps * k3[v]) for v in self.state_vars])
        a_new = self.get_aux(t + eps, x_new, u)
        values = [t + eps] + list(x_new.values()) + list(u.values()) + list(a_new.values())
        k4 = {}
        for v, eq in self.f.items():
            k4[v] = eq(*values)

        x_new = dict([(v, x[v] + (k1[v] + 2.0 * k2[v] + 2.0 * k3[v] + k4[v]) * (eps / 6.0)) for v in self.state_vars])

        return x_new

    def simulate(self, params):
        for v in self.control_vars:
            self.controllers[v].set_parameters(params)
        eps = self.sampling_eps
        max_steps = self.sampling_max_steps
        x0 = dict([(v, self.initial_conditions[v]) for v in self.state_vars])
        times = [0.0]
        states = [x0]
        controls = []
        errors_terminal_state = 0.0
        for step_id in range(1, max_steps + 1):
            t = times[-1]
            x = states[-1]
            u = dict([self.controllers[v].get_control(t, x) for v in self.control_vars])
            for v in self.control_vars:
                u[v] = DynamicSystem.constrain(u[v], self.control_bounds[v])
            a = self.get_aux(t, x, u)
            x_next = self.prolong(t, x, u, a, eps)
            times.append(t + eps)
            states.append(x_next)
            controls.append(u)
            if len(self.terminal_constraints) != 0:
                errors_terminal_state = []
                stop = True
                for constraint in self.terminal_constraints:
                    eq = constraint['equation']
                    max_error = constraint['max_error']
                    penalty = constraint['penalty']
                    norm = constraint['norm']

                    values = [times[-1]] + list(x_next.values())
                    error = DynamicSystem.measure_error(eq(*values))
                    if error > max_error:
                        stop = False
                        errors_terminal_state.append(np.power(penalty * error, float(norm[1:])))
                    else:
                        errors_terminal_state.append(error)
                if stop:
                    break
        I_integral = [states[-1]['I_integral_{}'.format(i + 1)] for i in range(len(self.integral_criteria))]
        I_terminal = self.terminal_criterion(*([times[-1]] + list(states[-1].values())))
        if isinstance(I_terminal, np.ndarray):
            I_terminal = I_terminal.tolist()
        phase_errors = [states[-1]['phase_{}'.format(i + 1)] for i in range(len(self.phase_constraints))]
        states = [dict((k, v) for (k, v) in s.items() if not k.startswith('I_integral_') and not k.startswith('phase_')) for s in states]
        controller_variance = []
        for c in self.controllers.values():
            if c.penalty == 0.0:
                controller_variance.append(0.0)
            else:
                controller_variance.append(c.penalty * c.get_measure_variance(times, states))
        return times, states, controls, I_integral, I_terminal, errors_terminal_state, phase_errors, controller_variance
