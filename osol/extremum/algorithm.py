"""Abstract algorithm definition with all desired functional."""

import json
from abc import ABC, abstractmethod

from osol.extremum.tools.coding import DecodeToNumpy, EncodeFromNumpy


class TerminationException(Exception):
    """Termination error."""


class OptimizationAlgorithm(ABC):
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

    def serialize(self):
        """Serialize current state."""
        return json.dumps(self.__dict__, indent=4, cls=EncodeFromNumpy)

    def deserialize(self, state):
        """Deserialize state from JSON deserialized dict."""
        self.__dict__ = json.loads(state, cls=DecodeToNumpy)

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
