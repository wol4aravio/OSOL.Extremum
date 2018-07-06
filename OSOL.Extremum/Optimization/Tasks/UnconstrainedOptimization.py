from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

import json


class UnconstrainedOptimization(dict):

    def __init__(self, f_str, vars_str):
        self._f_str = f_str
        self._vars_str = vars_str

        self._f_expr = parse_expr(f_str)
        self._sym_vars = list(map(symbols, vars_str))
        self._vars_str = vars_str
        self._f = lambdify(self._sym_vars, self._f_expr, np)

        dict.__init__(self, {'Task': {
            'name': 'UnconstrainedOptimization',
            'f_str': self._f_str,
            'vars_str': self._vars_str}})

    @classmethod
    def from_dict(cls, dict_data):
        return cls(f_str=dict_data['Task']['f_str'], vars_str=dict_data['Task']['vars_str'])

    @classmethod
    def from_json(cls, json_data):
        return UnconstrainedOptimization.from_dict(json.loads(json_data))

    def __call__(self, *args, **kwargs):
        vector = args[0]
        args = list(map(lambda v: vector[v], self._vars_str))
        return self._f(*args)
