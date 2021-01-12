"""Parser for *.opt files."""

import json

from sympy.parsing.latex import parse_latex


class OptTask:
    """Parsed *.opt task instance."""

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
        print(self._vars)
        self._check()

    def _check(self):
        self(*[0] * self._n_vars)

    def __call__(self, *args, **kwargs):
        min_length = min(len(self._vars), len(args))
        arg_values = {self._vars[i]: args[i] for i in range(min_length)}
        arg_values = {**arg_values, **kwargs}
        if len(arg_values) != self._n_vars:
            raise ValueError("Not enough variables")
        return self._f.evalf(subs=arg_values)
