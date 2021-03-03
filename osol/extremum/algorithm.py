import json
from abc import ABC, abstractmethod

from osol.extremum.tools.coding import DecodeToNumpy, EncodeFromNumpy


class TerminationException(Exception):
    pass


class OptimizationAlgorithm(ABC):
    @abstractmethod
    def initialize(self, f, search_area):
        raise NotImplementedError()

    @abstractmethod
    def iterate(self, f, search_area):
        raise NotImplementedError()

    @abstractmethod
    def terminate(self, f, search_area):
        raise NotImplementedError()

    def serialize(self):
        return json.dumps(self.__dict__, indent=4, cls=EncodeFromNumpy)

    def deserialize(self, state):
        self.__dict__ = json.loads(state, cls=DecodeToNumpy)

    def optimize(self, f, search_area, number_of_iterations, **kwargs):
        if not kwargs.get("skip_init", False):
            self.initialize(f, search_area)
        for _ in range(number_of_iterations):
            try:
                self.iterate(f, search_area)
            except TerminationException:
                break
        solution = self.terminate(f, search_area)
        return solution
