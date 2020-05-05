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


class BoxBettsQuadraticSum(Benchmark):
    """BoxBettsQuadraticSum benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.array([(0.9, 1.2), (9.0, 11.2), (0.9, 1.2)]),
            solution_x=np.array([1.0, 10.0, 1.0]),
            solution_y=0,
        )

    @staticmethod
    def _g(i, x):
        return (
            np.exp(-0.1 * (i + 1) * x[0])
            - np.exp(-0.1 * (i + 1) * x[1])
            - (np.exp(-0.1 * (i + 1)) - np.exp(-(i + 1)) * x[2])
        )

    def __call__(self, x):
        D = 10
        temp = np.array([BoxBettsQuadraticSum._g(i, x) for i in range(D)])
        return np.square(temp).sum()


class BraninRCOS(Benchmark):
    """BraninRCOS benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.array([(-5.0, 10.0), (0.0, 15.0)]),
            solution_x=np.array([-np.pi, 12.275]),
            solution_y=0.39788735772973816,
        )

    def __call__(self, x):
        return (
            (
                x[1]
                - 5.1 * x[0] * x[0] / (4 * np.pi * np.pi)
                + 5 * x[0] / np.pi
                - 6
            )
            * (
                x[1]
                - 5.1 * x[0] * x[0] / (4 * np.pi * np.pi)
                + 5 * x[0] / np.pi
                - 6
            )
            + 10.0 * (1.0 - 1.0 / (8.0 * np.pi)) * np.cos(x[0])
            + 10.0
        )


class Brent(Benchmark):
    """Brent benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-10.0, 10.0)),
            solution_x=np.full(shape=(2), fill_value=-10),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            (x[0] + 10.0) * (x[0] + 10.0)
            + (x[1] + 10.0) * (x[1] + 10.0)
            + np.exp(-x[0] * x[0] - x[1] * x[1])
        )


class Brown(Benchmark):
    """Brown benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-1.0, 4.0)),
            solution_x=np.full(shape=(n), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        part_1 = x[:-1]
        part_2 = x[1:]
        return np.sum(
            np.power(np.square(part_1), part_2 * part_2 + 1.0)
            + np.power(np.square(part_2), part_1 * part_1 + 1.0)
        )


class Bukin(Benchmark):
    """Bukin benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.array([(-15.0, -5.0), (-3.0, 3.0)]),
            solution_x=np.array([-10.0, 0.0]),
            solution_y=0,
        )

    def __call__(self, x):
        return 100 * x[1] ** 2 + 0.01 * np.abs(x[0] + 10)


class CamelThreeHumps(Benchmark):
    """CamelThreeHumps benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-5.0, 5.0)),
            solution_x=np.full(shape=(2), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            2.0 * x[0] * x[0]
            - 1.05 * x[0] * x[0] * x[0] * x[0]
            + x[0] * x[0] * x[0] * x[0] * x[0] * x[0] / 6.0
            + x[0] * x[1]
            + x[1] * x[1]
        )


class Chichinadze(Benchmark):
    """Chichinadze benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-30.0, 30.0)),
            solution_x=np.array([6.1898665869658, 0.5]),
            solution_y=-42.94438701899098,
        )

    def __call__(self, x):
        return (
            x[0] * x[0]
            - 12.0 * x[0]
            + 11.0
            + 10.0 * np.cos(np.pi * x[0] / 2.0)
            + 8.0 * np.sin(5.0 * np.pi * x[0] / 2.0)
            - np.sqrt(0.2) * np.exp(-0.5 * (x[1] - 0.5) * (x[1] - 0.5))
        )


class Colville(Benchmark):
    """Colville benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(4, 2), fill_value=(-10.0, 10.0)),
            solution_x=np.full(shape=(4), fill_value=1),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            100.0 * (x[0] - x[1] * x[1]) * (x[0] - x[1] * x[1])
            + (1.0 - x[0]) * (1.0 - x[0])
            + 90.0 * (x[3] - x[2] * x[2]) * (x[3] - x[2] * x[2])
            + (1.0 - x[2]) * (1.0 - x[2])
            + 10.1
            * ((x[1] - 1.0) * (x[1] - 1.0) + (x[3] - 1.0) * (x[3] - 1.0))
            + 19.8 * (x[1] - 1.0) * (x[3] - 1.0)
        )


class Corana(Benchmark):
    """Corana benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(4, 2), fill_value=(-500.0, 500.0)),
            solution_x=np.full(shape=(4), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        d = np.array([1.0, 1000.0, 10.0, 100.0])
        z = 0.2 * (np.abs(x / 0.2) + 0.49999) * np.sign(x)
        x = np.abs(x - z)
        A = 0.05
        part_1 = (np.abs(x) < A) * (
            0.15 * (z - 0.05 * np.sign(z)) * (z - 0.05 * np.sign(z)) * d
        )
        part_2 = (np.abs(x) >= A) * (d * np.square(x))
        return np.sum(part_1 + part_2)


class CosineMixture(Benchmark):
    """CosineMixture benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-1, 1)),
            solution_x=np.full(shape=(n), fill_value=0),
            solution_y=(-0.1 * n),
        )

    def __call__(self, x):
        return np.sum(-(0.1 * np.cos(5.0 * np.pi * x) - x * x))


class Csendes(Benchmark):
    """Csendes benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-1, 1)),
            solution_x=np.full(shape=(n), fill_value=1e-17),
            solution_y=0,
        )

    def __call__(self, x):
        return (np.power(x, 6.0) * (2.0 + np.sin(1.0 / x))).sum()


class Cube(Benchmark):
    """Cube benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-10.0, 10.0)),
            solution_x=np.full(shape=(2), fill_value=1),
            solution_y=0,
        )

    def __call__(self, x):
        return 100.0 * (x[1] - x[0] * x[0] * x[0]) * (
            x[1] - x[0] * x[0] * x[0]
        ) + (1.0 - x[0]) * (1.0 - x[0])


class Damavandi(Benchmark):
    """Damavandi benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(0.0, 14.0)),
            solution_x=np.full(shape=(2), fill_value=(2.0 + 1e-9)),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            1.0
            - np.power(
                np.abs(
                    ((np.sin(np.pi * (x[0] - 2))) * np.sin(np.pi * (x[0] - 2)))
                    / (np.pi * np.pi * (x[0] - 2.0) * (x[1] - 2.0))
                ),
                5,
            )
        ) * (
            2.0
            + (x[0] - 7.0) * (x[0] - 7.0)
            + 2.0 * (x[1] - 7.0) * (x[1] - 7.0)
        )


class Deb(Benchmark):
    """Deb benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-1, 1)),
            solution_x=np.full(shape=(n), fill_value=-0.9),
            solution_y=-1,
        )

    def __call__(self, x):
        return (-np.power(np.sin(5.0 * np.pi * x), 6.0) / len(x)).sum()


class DeckkersAarts(Benchmark):
    """DeckkersAarts benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-20, 20)),
            solution_x=np.array([0.0, 15.0]),
            solution_y=-24771.09375,
        )

    def __call__(self, x):
        return (
            100000.0 * x[0] * x[0]
            + x[1] * x[1]
            - (x[0] * x[0] + x[1] * x[1]) * (x[0] * x[0] + x[1] * x[1])
            + 0.00001 * np.power(x[0] * x[0] + x[1] * x[1], 4)
        )


class DixonAndPrice(Benchmark):
    """DixonAndPrice benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-10, 10)),
            solution_x=np.array(
                [
                    np.power(
                        2.0,
                        -(np.power(2.0, i + 1) - 2.0) / np.power(2.0, i + 1),
                    )
                    for i in range(n)
                ]
            ),
            solution_y=0,
        )

    def __call__(self, x):
        part_1 = x[1:]
        part_2 = x[:-1]
        return (x[0] - 1.0) * (x[0] - 1.0) + (
            np.arange(2, len(x) + 1)
            * np.square(2.0 * np.square(part_1) - part_2)
        ).sum()


class Dolan(Benchmark):
    """Dolan benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(5, 2), fill_value=(-100, 100)),
            solution_x=np.array(
                [
                    98.964258312237106,
                    100,
                    100,
                    99.224323672554704,
                    -0.249987527588471,
                ]
            ),
            solution_y=-529.8714387324576,
        )

    def __call__(self, x):
        return (
            (x[0] + 1.7 * x[1]) * np.sin(x[0])
            - 1.5 * x[2]
            - 0.1 * x[3] * np.cos(x[4] + x[3] - x[0])
            + 0.2 * x[4] * x[4]
            - x[1]
            - 1.0
        )


class Easom(Benchmark):
    """Easom benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-10, 10)),
            solution_x=np.full(shape=(2), fill_value=np.pi),
            solution_y=-1,
        )

    def __call__(self, x):
        return (
            -np.cos(x[0])
            * np.cos(x[1])
            * np.exp(-np.square(x[0] - np.pi) - np.square(x[1] - np.pi))
        )


class EggCrate(Benchmark):
    """EggCrate benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-5, 5)),
            solution_x=np.full(shape=(2), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            x[0] * x[0]
            + x[1] * x[1]
            + 25.0
            * (np.sin(x[0]) * np.sin(x[0]) + np.sin(x[1]) * np.sin(x[1]))
        )


class EggHolder(Benchmark):
    """EggHolder benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-512, 512)),
            solution_x=np.array([512.0, 404.2319]),
            solution_y=-959.640662709941,
        )

    def __call__(self, x):
        return -(x[1] + 47.0) * np.sin(
            np.sqrt(np.abs(x[1] + x[0] / 2.0 + 47.0))
        ) - x[0] * np.sin(np.sqrt(np.abs(x[0] - (x[1] + 47.0))))


class Exponential(Benchmark):
    """Exponential benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-1, 1)),
            solution_x=np.full(shape=(n), fill_value=0),
            solution_y=-1,
        )

    def __call__(self, x):
        return -np.exp((-0.5 * np.square(x)).sum())


class Goldstein(Benchmark):
    """Goldstein benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-2, 2)),
            solution_x=np.array([0.0, -1.0]),
            solution_y=3.0,
        )

    def __call__(self, x):
        return (
            1.0
            + (x[0] + x[1] + 1.0)
            * (x[0] + x[1] + 1.0)
            * (
                19.0
                - 14.0 * x[0]
                + 3.0 * x[0] * x[0]
                - 14.0 * x[1]
                + 6.0 * x[0] * x[1]
                + 3.0 * x[1] * x[1]
            )
        ) * (
            30.0
            + (2.0 * x[0] - 3 * x[1])
            * (2.0 * x[0] - 3 * x[1])
            * (
                18.0
                - 32.0 * x[0]
                + 12.0 * x[0] * x[0]
                + 48.0 * x[1]
                - 36 * x[0] * x[1]
                + 27.0 * x[1] * x[1]
            )
        )


class Griewank(Benchmark):
    """Griewank benchmark."""

    def __init__(self, n):
        super().__init__(
            search_area=np.full(shape=(n, 2), fill_value=(-100, 100)),
            solution_x=np.full(shape=(n), fill_value=0),
            solution_y=0,
        )

    def __call__(self, x):
        return (
            1.0
            + np.sum((np.square(x) / 4000.0))
            - np.prod(np.cos(x / np.sqrt(1 + np.arange(len(x)))))
        )


class GulfResearch(Benchmark):
    """GulfResearch benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.array([(0.1, 100.0), (0.0, 25.6), (0.0, 5.0)]),
            solution_x=np.array([50.0, 25.0, 1.5]),
            solution_y=0.0,
        )

    def __call__(self, x):
        i = np.arange(1, 100)
        u = 25.0 + np.power(-50.0 * np.log(0.01 * i), 1.0 / 1.5)
        return np.square(
            np.exp(-np.power(u - x[1], x[2]) / x[0]) - 0.01 * i
        ).sum()


class Hansen(Benchmark):
    """Hansen benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-10, 10)),
            solution_x=np.array([-7.58989583, -7.70831466]),
            solution_y=-176.54179313664181,
        )

    def __call__(self, x):
        i = np.arange(5)
        part_1 = (i + 1) * np.cos(i * x[0] + i + 1.0)
        part_2 = (i + 1) * np.cos((i + 2) * x[1] + i + 1.0)
        return part_1.sum() * part_2.sum()


class HelicalValley(Benchmark):
    """HelicalValley benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(3, 2), fill_value=(-100, 100)),
            solution_x=np.array([1.0, 0.0, 0.0]),
            solution_y=0,
        )

    def __call__(self, x):
        if x[0] >= 0.0:
            theta = np.arctan(x[1] / x[0]) / (2.0 * np.pi)
        else:
            theta = (np.pi + np.arctan(x[1] / x[0])) / (2.0 * np.pi)
        return (
            100.0
            * (
                np.square(x[2] - 10.0 * theta)
                + np.square(np.sqrt(x[0] * x[0] + x[1] * x[1]) - 1.0)
            )
            + x[2] * x[2]
        )


class Himmelblau(Benchmark):
    """Himmelblau benchmark."""

    def __init__(self):
        super().__init__(
            search_area=np.full(shape=(2, 2), fill_value=(-5, 5)),
            solution_x=np.array([3.0, 2.0]),
            solution_y=0,
        )

    def __call__(self, x):
        return np.square(x[0] * x[0] + x[1] - 11.0) + np.square(
            x[0] + x[1] * x[1] - 7.0
        )
