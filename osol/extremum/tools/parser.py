"""Parser for *.opt files."""

import json

import numpy as np
from sympy.parsing.latex import parse_latex


class OptTask:
    """Parsed task instance."""

    @staticmethod
    def from_file(filename):
        """Create OptTask from file."""
        with open(filename, "r") as opt_file:
            parsed = json.load(opt_file)
        return OptTask(parsed)

    def __init__(self, function_description):
        """Initialization."""
        self._f = parse_latex(function_description["function"])
        self._vars = function_description["vars"]
        self._n_vars = len(function_description["vars"])
        self._check()

    def _check(self):
        self([0] * self._n_vars)

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (list, np.ndarray)):
            args_ = [*args[0]]
        else:
            args_ = args
        min_length = min(len(self._vars), len(args_))
        arg_values = {self._vars[i]: args_[i] for i in range(min_length)}
        arg_values = {**arg_values, **kwargs}
        if len(arg_values) != self._n_vars:
            raise ValueError("Not enough variables")
        value = self._f.evalf(subs=arg_values)
        return value
