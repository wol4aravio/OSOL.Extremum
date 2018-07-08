from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

import json


class UnconstrainedOptimization:

    def __init__(self, f, variables):
        self._f = f
        self._variables = variables

        self._f_expr = parse_expr(f)
        self._sym_vars = list(map(symbols, variables))
        self._f_lambda = lambdify(self._sym_vars, self._f_expr, np)

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data)

    @classmethod
    def from_json(cls, json_data):
        return UnconstrainedOptimization.from_dict(json.loads(json_data)['UnconstrainedOptimization'])

    def __call__(self, *args, **kwargs):
        vector = args[0]
        args = list(map(lambda v: vector[v], self._variables))
        return self._f_lambda(*args)
