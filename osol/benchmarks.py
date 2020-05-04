"""Set of optimization benchmarks."""

from abc import ABC, abstractmethod

import numpy as np


class Benchmark(ABC):
    """Class for benchmark functions."""

    def __init__(self, search_area, solution_x, solution_y):
        """Benchmark initialization."""
        self.search_area = search_area
        self.solution_x = solution_x
        self.solution_y = solution_y

    @abstractmethod
    def __call__(self, x):
        """Function caller."""


class Ackley(Benchmark):
    """Ackley benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-35, 35)),
            solution_x=np.full(shape=(n), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        mean_pow = np.square(x).mean()
        mean_cos = np.cos(2 * np.pi * x).mean()
        return (
            -20.0 * np.exp(-0.02 * np.sqrt(mean_pow))
            - np.exp(mean_cos)
            + 20.0
            + np.e
        )


class Alpine(Benchmark):
    """Alpine benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-10, 10)),
            solution_x=np.full(shape=(n), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        return np.abs(x * np.sin(x) + 0.1 * x).sum()


class BartelsConn(Benchmark):
    """BartelsConn benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-500, 500)),
            solution_x=np.full(shape=(2), fill_value=0),
            solution_y=1,
        )

    def __call__(self, x):
        return (
            np.abs(x[0] * x[0] + x[1] * x[1] + x[0] * x[1])
            + np.abs(np.sin(x[0]))
            + np.abs(np.cos(x[1]))
        )
