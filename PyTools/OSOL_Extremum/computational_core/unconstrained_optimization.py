from sympy import symbols, lambdify, diff
from sympy.parsing.sympy_parser import parse_expr
import numpy as np


class UnconstrainedOptimization:

    def __init__(self, f_str, vars_str, first_derivative=False):
        self.f_expr = parse_expr(f_str)
        self.sym_vars = list(map(symbols, vars_str))
        self.vars_str = vars_str
        self._f = lambdify(self.sym_vars, self.f_expr, np)
        if first_derivative:
            self._df = {}
            derivatives = []
            for v in self.sym_vars:
                derivatives.append(diff(self.f_expr, v))
                self._df[str(v)] = lambdify(self.sym_vars, derivatives[-1], np)
            self._df['grad'] = lambdify(self.sym_vars, derivatives, np)

    def f(self, values):
        args = list(map(lambda v: values[v], self.vars_str))
        return self._f(*args)

    def df(self, d_name, values):
        args = list(map(lambda v: values[v], self.vars_str))
        return self._df[d_name](*args)

    @classmethod
    def from_dict(cls, data):
        if 'differentiable' in data:
            first_derivative = data['differentiable']
        else:
            first_derivative = False
        return cls(data['f'], data['vars'], first_derivative)
