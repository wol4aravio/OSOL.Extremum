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
        f.add_termination_criterion(
            TerminationViaAlgorithmIterations(number_of_iterations)
        )
        if not kwargs.get("skip_init", False):
            self.initialize(f, search_area)
        for iteration_id in range(number_of_iterations):
            f.termination_criteria[-1].set_current_iteration(iteration_id + 1)
            try:
                self.iterate(f, search_area)
            except TerminationException:
                break
        solution = self.terminate(f, search_area)
        return solution
