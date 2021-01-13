"""Tools for modification of functions with termination."""


class TerminationException(Exception):
    """Termination error."""


class TerminationViaAlgorithmIterations:
    """Function caller with external iteration counter."""

    def __init__(self, f, max_iterations):
        """Initialize via max_iterations."""
        self._f = f
        self._current_iteration = 0
        self._max_iterations = max_iterations

    def set_current_iteration(self, iteration):
        """Modifies current iteration."""
        self._current_iteration = iteration

    def __call__(self, x):
        """Apply function to argument."""
        if self._current_iteration >= self._max_iterations:
            raise TerminationException()
        return self._f(x)


class TerminationViaMaxCalls:
    """Function caller with limit."""

    def __init__(self, f, max_calls):
        """Initialize via max_calls."""
        self._f = f
        self._number_of_calls = 0
        self._max_calls = max_calls

    def __call__(self, x):
        """Apply function to argument."""
        if self._number_of_calls >= self._max_calls:
            raise TerminationException()
        self._number_of_calls += 1
        return self._f(x)
