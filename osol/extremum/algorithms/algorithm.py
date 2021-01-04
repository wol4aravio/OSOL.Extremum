"""Abstract algorithm definition with all desired functional."""


from abc import ABC, abstractmethod

from osol.extremum.algorithms.termination import TerminationException


class Algorithm(ABC):
    """Optimization algorithm."""

    @abstractmethod
    def initialize(self, f, search_area):
        """Initialization step."""

    @abstractmethod
    def iterate(self, f, search_area):
        """Iterative step."""

    @abstractmethod
    def terminate(self, f, search_area):
        """Termination step"""

    @abstractmethod
    def serialize(self):
        """Serialize current state."""

    @abstractmethod
    def deserialize(self, state_file):
        """Deserialize state from file."""

    def optimize(self, f, search_area, number_of_iterations, **kwargs):
        """Optimization procedure."""
        if not kwargs.get("skip_init", False):
            self.initialize(f, search_area)
        for _ in range(number_of_iterations):
            try:
                self.iterate(f, search_area)
            except TerminationException:
                break
        solution = self.terminate(f, search_area)
        return solution
