import json

from sympy import symbols, lambdify, diff
from sympy.parsing.sympy_parser import parse_expr
import numpy as np


class UnconstrainedOptimization:

    def __init__(self, f_str, vars_str, first_derivative=False):
        self.f_expr = parse_expr(f_str)
        self.sym_vars = list(map(symbols, vars_str))
        self.f = lambdify(self.sym_vars, self.f_expr, np)
        if first_derivative:
            self.df = {}
            derivatives = []
            for v in self.sym_vars:
                derivatives.append(diff(self.f_expr, v))
                self.df[str(v)] = lambdify(self.sym_vars, derivatives[-1], np)
            self.df['grad'] = lambdify(self.sym_vars, derivatives, np)

    @classmethod
    def from_json(cls, json_file):
        with open(json_file) as json_data:
            data = json.load(json_data)
            if 'differentiable' in data:
                first_derivative = data['differentiable']
            else:
                first_derivative = False
            return cls(data['f'], data['vars'], first_derivative)
