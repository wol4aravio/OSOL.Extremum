"""Tools for modification of functions with termination."""

from abc import ABC, abstractmethod
from datetime import datetime as dt


class TerminationException(Exception):
    """Termination error."""


class TerminationCriterion(ABC):
    """Basic class for terminations."""

    @abstractmethod
    def __call__(self):
        """Check criterion."""

    @abstractmethod
    def get_completeness(self):
        """Returns percentage of termination criterion fullfillness."""


class TerminationViaAlgorithmIterations(TerminationCriterion):
    """Function caller with external iteration counter."""

    def __init__(self, max_iterations):
        """Initialize via max_iterations."""
        self._current_iteration = 0
        self._max_iterations = max_iterations

    def __call__(self):
        """Check criterion."""
        if self._current_iteration >= self._max_iterations:
            raise TerminationException()

    def set_current_iteration(self, iteration):
        """Modifies current iteration."""
        self._current_iteration = iteration

    def get_completeness(self):
        return self._current_iteration / self._max_iterations


class TerminationViaMaxCalls(TerminationCriterion):
    """Function caller with limit."""

    def __init__(self, max_calls):
        """Initialize via max_calls."""
        self._number_of_calls = 0
        self._max_calls = max_calls

    def __call__(self):
        """Check criterion."""
        if self._number_of_calls >= self._max_calls:
            raise TerminationException()
        self._number_of_calls += 1

    def get_completeness(self):
        return self._number_of_calls / self._max_calls


class TerminationViaMaxTime(TerminationCriterion):
    """Function caller with limit."""

    def __init__(self, max_seconds):
        """Initialize via max_seconds."""
        self._start = dt.utcnow()
        self._max_seconds = max_seconds

    def __call__(self):
        """Check criterion."""
        if (dt.utcnow() - self._start).total_seconds() > self._max_seconds:
            raise TerminationException()

    def get_completeness(self):
        return (dt.utcnow() - self._start).total_seconds() / self._max_seconds
