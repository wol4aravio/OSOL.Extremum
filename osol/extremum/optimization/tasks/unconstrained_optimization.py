from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

from contracts import contract


class UnconstrainedOptimization:
    """ Task: optimization of a function without additional constraints on the domain"""

    @contract
    def __init__(self, f, variables):
        """ Task initialization

        :param f: objective function string
        :type f: str

        :param variables: variables that are used
        :type variables: list(str)
        """
        self._f = f
        self._variables = variables

        self._f_expr = parse_expr(f)
        self._sym_vars = list(map(symbols, variables))
        self._f_lambda = lambdify(self._sym_vars, self._f_expr, np)

    def __call__(self, *args, **kwargs):
        """ Application of the constructed function """
        return self._f_lambda(*args, **kwargs)
