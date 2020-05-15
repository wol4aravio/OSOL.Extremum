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

    def optimize(self, f, search_area, number_of_iterations):
        """Optimization procedure."""
        self.initialize(f, search_area)
        for _ in range(number_of_iterations):
            try:
                self.iterate(f, search_area)
            except TerminationException:
                break
        solution = self.terminate(f, search_area)
        return solution
