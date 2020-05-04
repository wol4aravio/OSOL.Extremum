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


class Beale(Benchmark):
    """Beale benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-4.5, 4.5)),
            solution_x=np.array([3.0, 0.5]),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            (1.5 - x[0] + x[0] * x[1]) * (1.5 - x[0] + x[0] * x[1])
            + (2.25 - x[0] + x[0] * x[1] * x[1])
            * (2.25 - x[0] + x[0] * x[1] * x[1])
            + (2.625 - x[0] + x[0] * x[1] * x[1] * x[1])
            * (2.625 - x[0] + x[0] * x[1] * x[1] * x[1])
        )


class Bird(Benchmark):
    """Bird benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(
                shape=(2, 2), fill_value=(-2.0 * np.pi, 2.0 * np.pi)
            ),
            solution_x=np.array([4.70105575198105, 3.152946019601391]),
            solution_y=-106.76453671980346,
        )

    def __call__(self, x):
        return (
            np.sin(x[0]) * np.exp((1.0 - np.cos(x[1])) * (1.0 - np.cos(x[1])))
            + np.cos(x[1])
            * np.exp((1.0 - np.sin(x[0])) * (1.0 - np.sin(x[0])))
            + (x[0] - x[1]) * (x[0] - x[1])
        )


class Bohachevsky(Benchmark):
    """Bohachevsky benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-100, 100)),
            solution_x=np.full(shape=(2), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            x[0] * x[0]
            + 2 * x[1] * x[1]
            - 0.3 * np.cos(3.0 * np.pi * x[0])
            - 0.4 * np.cos(4 * np.pi * x[1])
            + 0.7
        )


class Booth(Benchmark):
    """Booth benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-10, 10)),
            solution_x=np.array([1.0, 3.0]),
            solution_y=0,
        )

    def __call__(self, x):
        return (x[0] + 2.0 * x[1] - 7.0) * (x[0] + 2.0 * x[1] - 7.0) + (
            2.0 * x[0] + x[1] - 5.0
        ) * (2.0 * x[0] + x[1] - 5.0)
