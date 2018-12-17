from abc import ABC, abstractmethod
from contracts import contract, ContractsMeta

from osol.extremum.etc.new_contracts import * # Inclusion of user defined contracts


class OptimizationBenchmark(ABC, metaclass=ContractsMeta):
    """ Abstract class that describes desired interface to benchmark functions """

    @abstractmethod
    @contract
    def call(self, v):
        """ Applies function to vector

            :param v: target vector
            :type v: Vector
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

            :rtype: tuple(Vector, number)
        """


@contract
def benchmark_algorithm(algorithm, benchmarks, terminator, number_of_runs):
    """ Performs benchmarking process

    :param algorithm: target algorithm
    :type algorithm: Algorithm

    :param benchmarks: benchmarks to be used
    :type benchmarks: dict(str:Benchmark)

    :param terminator: termination criterion generator
    :type terminator: *

    :param number_of_runs: how many times the algorithm should be tested
    :type number_of_runs: int

    :returns: algorithm application results
    :rtype: dict(str:tuple(list(tuple(Vector, number)),number))
    """
    results = dict()
    for b_name, b_func in benchmarks.items():
        search_area = b_func.search_area
        bt = terminator(b_func)
        results[b_name] = []
        for _ in range(number_of_runs):
            x = algorithm.optimize(bt, search_area)
            y = b_func(x)
            results[b_name].append((x, y))
        results[b_name] = (results[b_name], b_func.solution[1])
    return results
