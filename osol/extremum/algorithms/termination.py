"""Tools for modification of functions with termination."""


from abc import ABC, abstractmethod


class TerminationException(Exception):
    """Termination error."""


class TerminationCriterion(ABC):
    """Basic class for terminations."""

    def __init__(self):
        self._callbacks = list()

    def add_callback(self, callback):
        """Add callback."""
        self._callbacks.append(callback)

    def __call__(self, x):
        """Apply criterion callbacks."""
        for callback in self._callbacks:
            callback(self)

    @abstractmethod
    def get_completeness(self):
        """Returns percentage of termination criterion fullfillness."""


class TerminationViaAlgorithmIterations(TerminationCriterion):
    """Function caller with external iteration counter."""

    def __init__(self, f, max_iterations):
        """Initialize via max_iterations."""
        super().__init__()
        self._f = f
        self._current_iteration = 0
        self._max_iterations = max_iterations

    def set_current_iteration(self, iteration):
        """Modifies current iteration."""
        self._current_iteration = iteration

    def __call__(self, x):
        """Apply function to argument."""
        super().__call__(x)
        if self._current_iteration >= self._max_iterations:
            raise TerminationException()
        return self._f(x)

    def get_completeness(self):
        return self._current_iteration / self._max_iterations


class TerminationViaMaxCalls(TerminationCriterion):
    """Function caller with limit."""

    def __init__(self, f, max_calls):
        """Initialize via max_calls."""
        super().__init__()
        self._f = f
        self._number_of_calls = 0
        self._max_calls = max_calls

    def __call__(self, x):
        """Apply function to argument."""
        super().__call__(x)
        if self._number_of_calls >= self._max_calls:
            raise TerminationException()
        self._number_of_calls += 1
        return self._f(x)

    def get_completeness(self):
        return self._number_of_calls / self._max_calls
