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
    def initialize(self, f, f_grad, search_area):
        """Initialization step."""

    @abstractmethod
    def iterate(self, f, f_grad, search_area):
        """Iterative step."""

    @abstractmethod
    def terminate(self, f, f_grad, search_area):
        """Termination step"""

    def optimize(self, f, f_grad, search_area, number_of_iterations):
        """Optimization procedure."""
        self.initialize(f, f_grad, search_area)
        for _ in range(number_of_iterations):
            try:
                self.iterate(f, f_grad, search_area)
            except TerminationException:
                break
        solution = self.terminate(f, f_grad, search_area)
        return solution
