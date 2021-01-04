"""Parser for *.opt files."""

import json

from sympy.parsing.latex import parse_latex


class OptTask:
    """Parsed *.opt task instance."""

    def __init__(self, filename):
        """Initialization."""
        with open(filename, "r") as opt_file:
            parsed = json.load(opt_file)
        self._f = parse_latex(parsed["function"])
        self._vars = parsed["vars"]
        self._n_vars = len(parsed["vars"])

    def __call__(self, *args, **kwargs):
        min_length = min(len(self._vars), len(args))
        arg_values = {self._vars[i]: args[i] for i in range(min_length)}
        arg_values = {**arg_values, **kwargs}
        if len(arg_values) != self._n_vars:
            raise ValueError("Not enough variables")
        return self._f.evalf(subs=arg_values)
