"""Abstract algorithm definition with all desired functional."""


from abc import ABC, abstractmethod

from osol.extremum.algorithms.termination import (
    TerminationException,
    TerminationViaAlgorithmIterations,
)


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
    def deserialize(self, state):
        """Deserialize state from JSON deserialized dict."""

    def optimize(self, f, search_area, number_of_iterations, **kwargs):
        """Optimization procedure."""
        f_ = TerminationViaAlgorithmIterations(f, number_of_iterations)
        if not kwargs.get("skip_init", False):
            self.initialize(f_, search_area)
        iteration_id = 0
        while True:
            f_.set_current_iteration(iteration_id)
            try:
                self.iterate(f_, search_area)
            except TerminationException:
                break
            iteration_id += 1
        solution = self.terminate(f_, search_area)
        return solution
