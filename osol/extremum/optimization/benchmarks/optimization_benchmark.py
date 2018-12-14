from abc import ABC, abstractmethod
from contracts import contract, ContractsMeta

from osol.extremum.optimization.basic.vector import Vector # Required for `vector` contract inclusion


class OptimizationBenchmark(ABC, metaclass=ContractsMeta):
    """ Abstract class that describes desired interface to benchmark functions """

    @abstractmethod
    @contract
    def call(self, v):
        """ Applies function to vector

            :param v: target vector
            :type v: vector
        """

    def __call__(self, *args, **kwargs):
        return self.call(args[0])

    @property
    @abstractmethod
    @contract
    def search_area(self):
        """ Returns search area for current benchmark

            :rtype: dict(str:tuple(number, number))
        """

    @property
    @abstractmethod
    @contract
    def solution(self):
        """ Returns solution current benchmark

            :rtype: tuple(vector, number)
        """
