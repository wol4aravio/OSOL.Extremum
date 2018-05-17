from OSOL_Extremum.arithmetics.interval import *
from OSOL_Extremum.cybernatics.controllers import create_controller_from_dict

from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np


class DynamicSystem:

    def __init__(self,
                 sampling_type, sampling_eps, sampling_max_steps,
                 f, state_vars, initial_conditions,
                 controllers, control_vars, control_bounds,
                 aux, etc_vars,
                 integral_criterion, terminal_criterion,
                 terminal_constraints, phase_constraints):
        self.state_vars = state_vars
        self.control_vars = control_vars
        self.etc_vars = etc_vars
        self.vars_str = ['t'] + self.state_vars + self.control_vars + self.etc_vars
        self.sym_vars = list(map(symbols, self.vars_str))

        self.initial_conditions = initial_conditions

        self.controllers = controllers
        self.control_bounds = control_bounds

        self.f = f
        for v in self.state_vars:
            self.f[v] = lambdify(self.sym_vars, parse_expr(self.f[v]), np)

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

        self.integral_criterion = lambdify(self.sym_vars, parse_expr(integral_criterion), np)
        self.terminal_criterion = lambdify(self.sym_vars, parse_expr(terminal_criterion), np)

        self.terminal_constraints = terminal_constraints
        for i in range(len(self.terminal_constraints)):
            self.terminal_constraints[i]['equation'] = lambdify(self.sym_vars, self.terminal_constraints[i]['equation'], np)

        self.phase_constraints = phase_constraints
        for i in range(len(self.terminal_constraints)):
            self.phase_constraints[i]['equation'] = lambdify(self.sym_vars, self.phase_constraints[i]['equation'], np)


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
        for d in data['constraints']['terminal']:
            constraint = dict()
            constraint['equation'] = d['equation']
            constraint['max_error'] = d['max_error']
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
        for step_id in range(1, max_steps + 1):
            t = times[-1]
            x = states[-1]
            u = dict([self.controllers[v].get_control(t, x) for v in self.control_vars])
            a = self.get_aux(t, x, u)
            x_next = self.prolong(t, x, u, a, eps)
            times.append(t + eps)
            states.append(x_next)
            controls.append(u)
        return times, states, controls
