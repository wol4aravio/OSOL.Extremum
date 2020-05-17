"""Template for algorithm development"""

from abc import ABC, abstractmethod

from osol.algorithms.termination import TerminationException


class AlgorithmZeroOrder(ABC):
    """Basic class for all optimization algorithms."""

    @abstractmethod
    def initialize(self, f, search_area):
        """Initialization step."""

    @abstractmethod
    def iterate(self, f, search_area):
        """Iterative step."""

    @abstractmethod
    def terminate(self, f, search_area):
        """Termination step"""

    def _get_trace_attributes(self):
        """Save all non-private attributes."""
        names = [a for a in dir(self) if not a.startswith("_")]
        names = [
            a
            for a in names
            if a
            not in ("trace", "initialize", "iterate", "terminate", "optimize")
        ]
        values = {n: getattr(self, n) for n in names}
        self.trace.append(values)

    def optimize(self, f, search_area, number_of_iterations, save_trace=False):
        """Optimization procedure."""
        self.trace = None
        self.initialize(f, search_area)
        if save_trace:
            self.trace = list()
            self._get_trace_attributes()
        else:
            self.trace = None
        for _ in range(number_of_iterations):
            try:
                self.iterate(f, search_area)
                if save_trace:
                    self._get_trace_attributes()
            except TerminationException:
                break
        solution = self.terminate(f, search_area)
        if save_trace:
            self._get_trace_attributes()
        return solution


class AlgorithmFirstOrder(ABC):
    """Basic class for all optimization algorithms."""

    @abstractmethod
    def initialize(self, f, g, search_area):
        """Initialization step."""

    @abstractmethod
    def iterate(self, f, g, search_area):
        """Iterative step."""

    @abstractmethod
    def terminate(self, f, g, search_area):
        """Termination step"""

    def _get_trace_attributes(self):
        """Save all non-private attributes."""
        names = [a for a in dir(self) if not a.startswith("_")]
        names = [
            a
            for a in names
            if a
            not in ("trace", "initialize", "iterate", "terminate", "optimize")
        ]
        values = {n: getattr(self, n) for n in names}
        self.trace.append(values)

    def optimize(self, f, g, search_area, num_of_iterations, save_trace=False):
        """Optimization procedure."""
        self.trace = None
        self.initialize(f, g, search_area)
        if save_trace:
            self.trace = list()
            self._get_trace_attributes()
        else:
            self.trace = None
        for _ in range(num_of_iterations):
            try:
                self.iterate(f, g, search_area)
                if save_trace:
                    self._get_trace_attributes()
            except TerminationException:
                break
        solution = self.terminate(f, g, search_area)
        if save_trace:
            self._get_trace_attributes()
        return solution