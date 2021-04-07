from abc import ABC, abstractmethod

import numpy as np


class OptimizationBenchmark(ABC):
    @abstractmethod
    def call(self, v):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        return self.call(args[0])

    @property
    @abstractmethod
    def search_area(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def solution(self):
        raise NotImplementedError()


class VariableDimFunction:
    def __init__(self, n):
        self._n = n


def create_fix_dim_function(n):
    class FixDimFunction:
        def __init__(self):
            self._n = n

    return FixDimFunction


def create_search_area(v1, v2, n):
    return np.array([(v1, v2) for i in range(n)])


def create_symmetric_search_area(v, n):
    return create_search_area(v1=-v, v2=v, n=n)


def create_solution_vector(v, n):
    return np.array([v for _ in range(n)])


class Ackley(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        mean_pow = np.square(v).mean()
        mean_cos = np.cos(2 * np.pi * v).mean()
        return (
            -20.0 * np.exp(-0.02 * np.sqrt(mean_pow)) - np.exp(mean_cos) + 20.0 + np.e
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(35.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Alpine(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return np.abs(v * np.sin(v) + 0.1 * v).sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class BartelsConn(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            np.abs(v[0] * v[0] + v[1] * v[1] + v[0] * v[1])
            + np.abs(np.sin(v[0]))
            + np.abs(np.cos(v[1]))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(500.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 1.0


class Beale(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            (1.5 - v[0] + v[0] * v[1]) * (1.5 - v[0] + v[0] * v[1])
            + (2.25 - v[0] + v[0] * v[1] * v[1]) * (2.25 - v[0] + v[0] * v[1] * v[1])
            + (2.625 - v[0] + v[0] * v[1] * v[1] * v[1])
            * (2.625 - v[0] + v[0] * v[1] * v[1] * v[1])
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(4.5, self._n)

    @property
    def solution(self):
        return np.array([3.0, 0.5]), 0.0


class Bird(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            np.sin(v[0]) * np.exp((1.0 - np.cos(v[1])) * (1.0 - np.cos(v[1])))
            + np.cos(v[1]) * np.exp((1.0 - np.sin(v[0])) * (1.0 - np.sin(v[0])))
            + (v[0] - v[1]) * (v[0] - v[1])
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(2.0 * np.pi, self._n)

    @property
    def solution(self):
        return np.array([4.70105575198105, 3.152946019601391]), -106.76453671980346


class Bohachevsky(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            v[0] * v[0]
            + 2 * v[1] * v[1]
            - 0.3 * np.cos(3.0 * np.pi * v[0])
            - 0.4 * np.cos(4 * np.pi * v[1])
            + 0.7
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Booth(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (v[0] + 2.0 * v[1] - 7.0) * (v[0] + 2.0 * v[1] - 7.0) + (
            2.0 * v[0] + v[1] - 5.0
        ) * (2.0 * v[0] + v[1] - 5.0)

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return np.array([1.0, 3.0]), 0.0


class BoxBettsQuadraticSum(create_fix_dim_function(3), OptimizationBenchmark):
    @staticmethod
    def g(i, v):
        return (
            np.exp(-0.1 * (i + 1) * v[0])
            - np.exp(-0.1 * (i + 1) * v[1])
            - (np.exp(-0.1 * (i + 1)) - np.exp(-(i + 1)) * v[2])
        )

    def call(self, v):
        D = 10
        temp = np.array([BoxBettsQuadraticSum.g(i, v) for i in range(D)])
        return np.square(temp).sum()

    @property
    def search_area(self):
        return np.array([(0.9, 1.2), (9.0, 11.2), (0.9, 1.2)])

    @property
    def solution(self):
        return np.array([1.0, 10.0, 1.0]), 0.0


class BraninRCOS(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            (v[1] - 5.1 * v[0] * v[0] / (4 * np.pi * np.pi) + 5 * v[0] / np.pi - 6)
            * (v[1] - 5.1 * v[0] * v[0] / (4 * np.pi * np.pi) + 5 * v[0] / np.pi - 6)
            + 10.0 * (1.0 - 1.0 / (8.0 * np.pi)) * np.cos(v[0])
            + 10.0
        )

    @property
    def search_area(self):
        return np.array([(-5.0, 10.0), (0.0, 15.0)])

    @property
    def solution(self):
        return np.array([-np.pi, 12.275]), 0.39788735772973816


class Brent(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            (v[0] + 10.0) * (v[0] + 10.0)
            + (v[1] + 10.0) * (v[1] + 10.0)
            + np.exp(-v[0] * v[0] - v[1] * v[1])
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(-10.0, self._n), 0.0


class Brown(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        v1 = v[:-1]
        v2 = v[1:]
        return np.sum(
            np.power(np.square(v1), v2 * v2 + 1.0)
            + np.power(np.square(v2), v1 * v1 + 1.0)
        )

    @property
    def search_area(self):
        return create_search_area(-1.0, 4.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Bukin(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 100 * v[1] ** 2 + 0.01 * np.abs(v[0] + 10)

    @property
    def search_area(self):
        return np.array([(-15.0, -5.0), (-3.0, 3.0)])

    @property
    def solution(self):
        return np.array([-10.0, 0.0]), 0.0


class CamelThreeHumps(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            2.0 * v[0] * v[0]
            - 1.05 * v[0] * v[0] * v[0] * v[0]
            + v[0] * v[0] * v[0] * v[0] * v[0] * v[0] / 6.0
            + v[0] * v[1]
            + v[1] * v[1]
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(5.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Chichinadze(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            v[0] * v[0]
            - 12.0 * v[0]
            + 11.0
            + 10.0 * np.cos(np.pi * v[0] / 2.0)
            + 8.0 * np.sin(5.0 * np.pi * v[0] / 2.0)
            - np.sqrt(0.2) * np.exp(-0.5 * (v[1] - 0.5) * (v[1] - 0.5))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(30.0, self._n)

    @property
    def solution(self):
        return np.array([6.1898665869658, 0.5]), -42.94438701899098


class Colville(create_fix_dim_function(4), OptimizationBenchmark):
    def call(self, v):
        return (
            100.0 * (v[0] - v[1] * v[1]) * (v[0] - v[1] * v[1])
            + (1.0 - v[0]) * (1.0 - v[0])
            + 90.0 * (v[3] - v[2] * v[2]) * (v[3] - v[2] * v[2])
            + (1.0 - v[2]) * (1.0 - v[2])
            + 10.1 * ((v[1] - 1.0) * (v[1] - 1.0) + (v[3] - 1.0) * (v[3] - 1.0))
            + 19.8 * (v[1] - 1.0) * (v[3] - 1.0)
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(1.0, self._n), 0.0


class Corana(create_fix_dim_function(4), OptimizationBenchmark):
    def call(self, v):
        d = np.array([1.0, 1000.0, 10.0, 100.0])
        z = 0.2 * (np.abs(v / 0.2) + 0.49999) * np.sign(v)
        v = np.abs(v - z)
        A = 0.05
        part_1 = (np.abs(v) < A) * (
            0.15 * (z - 0.05 * np.sign(z)) * (z - 0.05 * np.sign(z)) * d
        )
        part_2 = (np.abs(v) >= A) * (d * np.square(v))
        return np.sum(part_1 + part_2)

    @property
    def search_area(self):
        return create_symmetric_search_area(500.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class CosineMixture(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return np.sum(-(0.1 * np.cos(5.0 * np.pi * v) - v * v))

    @property
    def search_area(self):
        return create_symmetric_search_area(1.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), -0.1 * self._n


class Csendes(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return (np.power(v, 6.0) * (2.0 + np.sin(1.0 / v))).sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(1.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(1e-9, self._n), 0.0


class Cube(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 100.0 * (v[1] - v[0] * v[0] * v[0]) * (v[1] - v[0] * v[0] * v[0]) + (
            1.0 - v[0]
        ) * (1.0 - v[0])

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(1.0, self._n), 0.0


class Damavandi(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            1.0
            - np.power(
                np.abs(
                    ((np.sin(np.pi * (v[0] - 2))) * np.sin(np.pi * (v[0] - 2)))
                    / (np.pi * np.pi * (v[0] - 2.0) * (v[1] - 2.0))
                ),
                5,
            )
        ) * (2.0 + (v[0] - 7.0) * (v[0] - 7.0) + 2.0 * (v[1] - 7.0) * (v[1] - 7.0))

    @property
    def search_area(self):
        return create_search_area(0.0, 14.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(2.0 + 1e-5, self._n), 0.0


class Deb(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return (-np.power(np.sin(5.0 * np.pi * v), 6.0) / self._n).sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(1.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(-0.9, self._n), -1.0


class DeckkersAarts(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            100000.0 * v[0] * v[0]
            + v[1] * v[1]
            - (v[0] * v[0] + v[1] * v[1]) * (v[0] * v[0] + v[1] * v[1])
            + 0.00001 * np.power(v[0] * v[0] + v[1] * v[1], 4)
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(20.0, self._n)

    @property
    def solution(self):
        return np.array([0.0, 15.0]), -24771.09375


class DixonAndPrice(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        v1 = v[1:]
        v2 = v[:-1]
        return (v[0] - 1.0) * (v[0] - 1.0) + (
            np.arange(2, self._n + 1) * np.square(2.0 * np.square(v1) - v2)
        ).sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return (
            np.array(
                [
                    np.power(2.0, -(np.power(2.0, i + 1) - 2.0) / np.power(2.0, i + 1))
                    for i in range(self._n)
                ]
            ),
            0.0,
        )


class Dolan(create_fix_dim_function(5), OptimizationBenchmark):
    def call(self, v):
        return (
            (v[0] + 1.7 * v[1]) * np.sin(v[0])
            - 1.5 * v[2]
            - 0.1 * v[3] * np.cos(v[4] + v[3] - v[0])
            + 0.2 * v[4] * v[4]
            - v[1]
            - 1.0
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return (
            np.array(
                [98.964258312237106, 100, 100, 99.224323672554704, -0.249987527588471]
            ),
            -529.8714387324576,
        )


class Easom(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            -np.cos(v[0])
            * np.cos(v[1])
            * np.exp(-np.square(v[0] - np.pi) - np.square(v[1] - np.pi))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(np.pi, self._n), -1.0


class EggCrate(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            v[0] * v[0]
            + v[1] * v[1]
            + 25.0 * (np.sin(v[0]) * np.sin(v[0]) + np.sin(v[1]) * np.sin(v[1]))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(5.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class EggHolder(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return -(v[1] + 47.0) * np.sin(np.sqrt(np.abs(v[1] + v[0] / 2.0 + 47.0))) - v[
            0
        ] * np.sin(np.sqrt(np.abs(v[0] - (v[1] + 47.0))))

    @property
    def search_area(self):
        return create_symmetric_search_area(512.0, self._n)

    @property
    def solution(self):
        return np.array([512.0, 404.2319]), -959.640662709941


class Exponential(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return -np.exp((-0.5 * np.square(v)).sum())

    @property
    def search_area(self):
        return create_symmetric_search_area(1.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), -1.0


class Goldstein(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            1.0
            + (v[0] + v[1] + 1.0)
            * (v[0] + v[1] + 1.0)
            * (
                19.0
                - 14.0 * v[0]
                + 3.0 * v[0] * v[0]
                - 14.0 * v[1]
                + 6.0 * v[0] * v[1]
                + 3.0 * v[1] * v[1]
            )
        ) * (
            30.0
            + (2.0 * v[0] - 3 * v[1])
            * (2.0 * v[0] - 3 * v[1])
            * (
                18.0
                - 32.0 * v[0]
                + 12.0 * v[0] * v[0]
                + 48.0 * v[1]
                - 36 * v[0] * v[1]
                + 27.0 * v[1] * v[1]
            )
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(2.0, self._n)

    @property
    def solution(self):
        return np.array([0.0, -1.0]), 3.0


class Griewank(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return (
            1.0
            + np.sum((np.square(v) / 4000.0))
            - np.prod(np.cos(v / np.sqrt(1 + np.arange(self._n))))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class GulfResearch(create_fix_dim_function(3), OptimizationBenchmark):
    def call(self, v):
        i = np.arange(1, 100)
        u = 25.0 + np.power(-50.0 * np.log(0.01 * i), 1.0 / 1.5)
        return np.square(np.exp(-np.power(u - v[1], v[2]) / v[0]) - 0.01 * i).sum()

    @property
    def search_area(self):
        return np.array([(0.1, 100.0), (0.0, 25.6), (0.0, 5.0)])

    @property
    def solution(self):
        return np.array([50.0, 25.0, 1.5]), 0.0


class Hansen(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        i = np.arange(5)
        p1 = (i + 1) * np.cos(i * v[0] + i + 1.0)
        p2 = (i + 1) * np.cos((i + 2) * v[1] + i + 1.0)
        return p1.sum() * p2.sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return np.array([-7.58989583, -7.70831466]), -176.54179313664181


class HelicalValley(create_fix_dim_function(3), OptimizationBenchmark):
    def call(self, v):
        if v[0] >= 0.0:
            theta = np.arctan(v[1] / v[0]) / (2.0 * np.pi)
        else:
            theta = (np.pi + np.arctan(v[1] / v[0])) / (2.0 * np.pi)
        return (
            100.0
            * (
                np.square(v[2] - 10.0 * theta)
                + np.square(np.sqrt(v[0] * v[0] + v[1] * v[1]) - 1.0)
            )
            + v[2] * v[2]
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return np.array([1.0, 0.0000000001, 0.0]), 0.0


class Himmelblau(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return np.square(v[0] * v[0] + v[1] - 11.0) + np.square(
            v[0] + v[1] * v[1] - 7.0
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(5.0, self._n)

    @property
    def solution(self):
        return np.array([3.0, 2.0]), 0.0


class Hosaki(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            (
                1.0
                - 8.0 * v[0]
                + 7 * v[0] * v[0]
                - 7.0 * v[0] * v[0] * v[0] / 3.0
                + 0.25 * v[0] * v[0] * v[0] * v[0]
            )
            * v[1]
            * v[1]
            * np.exp(-v[1])
        )

    @property
    def search_area(self):
        return np.array([(0.0, 5.0), (0.0, 6.0)])

    @property
    def solution(self):
        return np.array([4.0, 2.0]), -2.3458115458488518


class JennrichSampson(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        i = np.arange(1, 11)
        return np.square(2.0 + 2.0 * i - (np.exp(i * v[0]) + np.exp(i * v[1]))).sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(1.0, self._n)

    @property
    def solution(self):
        return np.array([0.257825, 0.257825]), 124.36218236258078


class Keane(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return np.square(np.sin(v[0] - v[1]) * np.sin(v[0] + v[1])) / np.sqrt(
            v[0] * v[0] + v[1] * v[1]
        )

    @property
    def search_area(self):
        return create_search_area(0.0, 10.0, self._n)

    @property
    def solution(self):
        return np.array([0.0, 1.39325]), 0.6736675


class Langermann(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        a = np.array([9.681, 9.4, 8.025, 2.196, 8.074])
        b = np.array([0.667, 2.041, 9.152, 0.415, 8.777])
        c = np.array([0.806, 0.517, 0.1, 0.908, 0.965])
        result = (
            c
            * np.cos(np.pi * ((v[0] - a) * (v[0] - a) + (v[1] - b) * (v[1] - b)))
            / np.exp(((v[0] - a) * (v[0] - a) + (v[1] - b) * (v[1] - b)) / np.pi)
        )
        return np.sum(-result)

    @property
    def search_area(self):
        return create_search_area(0.0, 10.0, self._n)

    @property
    def solution(self):
        return np.array([9.6810707, 0.6666515]), -1.08093846723926811925764468469


class Leon(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 100.0 * (v[1] - v[0] * v[0]) * (v[1] - v[0] * v[0]) + (1.0 - v[0]) * (
            1.0 - v[0]
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(1.2, self._n)

    @property
    def solution(self):
        return create_solution_vector(1.0, self._n), 0.0


class Matyas(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 0.26 * (v[0] * v[0] + v[1] * v[1]) - 0.48 * v[0] * v[1]

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class McCormick(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            np.sin(v[0] + v[1])
            + (v[0] - v[1]) * (v[0] - v[1])
            - v[0]
            + 2.0 * v[1]
            + 1.0
        )

    @property
    def search_area(self):
        return np.array([(-1.5, 4.0), (-3.0, 3.0)])

    @property
    def solution(self):
        return np.array([-0.5471975602214493, -1.547197559268372]), -1.413222955457575


class MieleCantrell(create_fix_dim_function(4), OptimizationBenchmark):
    def call(self, v):
        return (
            np.power(np.exp(-v[0]) - v[1], 4)
            + 100.0 * np.power(v[1] - v[2], 6)
            + np.power(np.tan(v[2] - v[3]), 4)
            + np.power(v[0], 8)
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(1.0, self._n)

    @property
    def solution(self):
        return np.array([0.0, 1.0, 1.0, 1.0]), 0.0


class MishraZeroSum(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return 100.0 * np.sqrt(np.abs(v.sum()))

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Parsopoulos(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return np.square(np.cos(v[0])) + np.square(np.sin(v[1]))

    @property
    def search_area(self):
        return create_symmetric_search_area(5.0, self._n)

    @property
    def solution(self):
        return np.array([np.pi / 2.0, 0.0]), 0.0


class PenHolder(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return -np.exp(
            -1.0
            / np.abs(
                np.cos(v[0])
                * np.cos(v[1])
                * np.exp(np.abs(1.0 - np.sqrt(v[0] * v[0] + v[1] * v[1]) / np.pi))
            )
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(11.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(9.646167671043401, self._n), -0.9635348327265058


class Pathological(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        v1 = v[:-1]
        v2 = v[1:]
        return np.sum(
            0.5
            + (np.square(np.sin(np.sqrt(100.0 * v1 * v1 + v2 * v2))) - 0.5)
            / (1.0 + 0.001 * np.square(v1 * v1 - 2 * v1 * v2 + v2 * v2))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Paviani(create_fix_dim_function(10), OptimizationBenchmark):
    def call(self, v):
        p1 = np.sum(np.square(np.log(v - 2.0)) + np.square(np.log(10.0 - v)))
        p2 = np.prod(v)
        return p1 - np.power(p2, 0.2)

    @property
    def search_area(self):
        return create_search_area(2.0001, 10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(9.351, self._n), -45.77845205382887


class Periodic(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            1.0
            + np.square(np.sin(v[0]))
            + np.square(np.sin(v[1]))
            - 0.1 * np.exp(-(v[0] * v[0] + v[1] * v[1]))
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.9


class Price(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (np.abs(v[0]) - 5.0) * (np.abs(v[0]) - 5.0) + (np.abs(v[1]) - 5.0) * (
            np.abs(v[1]) - 5.0
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(500.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(5.0, self._n), 0.0


class Quadratic(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            -3803.84
            - 138.08 * v[0]
            - 232.92 * v[1]
            + 128.08 * v[0] * v[0]
            + 203.64 * v[1] * v[1]
            + 182.25 * v[0] * v[1]
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return np.array([0.19388, 0.48513]), -3873.724182183056


class Quintic(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return np.abs(
            np.power(v, 5)
            - 3.0 * np.power(v, 4)
            + 4.0 * np.power(v, 3)
            + 2.0 * np.square(v)
            - 10.0 * v
            - 4.0
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(-1.0, self._n), 0.0


class Ripple(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        return -(
            np.exp(-2 * np.log(2) * np.square((v - 0.1) / 0.8))
            * (
                np.power(np.sin(5.0 * np.pi * v), 6)
                + 0.1 * np.square(np.cos(500.0 * np.pi * v))
            )
        ).sum()

    @property
    def search_area(self):
        return create_search_area(0.0, 1.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.1, self._n), -self._n * 1.1


class Rosenbrock(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        v1 = v[1:]
        v2 = v[:-1]
        return (100.0 * (v1 - v2 * v2) * (v1 - v2 * v2) + (v2 - 1.0) * (v2 - 1.0)).sum()

    @property
    def search_area(self):
        return create_symmetric_search_area(30.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(1.0, self._n), 0.0


class RosenbrockModified(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            74.0
            + 100.0 * (v[1] - v[0] * v[0]) * (v[1] - v[0] * v[0])
            + (1.0 - v[0]) * (1.0 - v[0])
            - 400.0 * np.exp(-((v[0] + 1) * (v[0] + 1) + (v[1] + 1) * (v[1] + 1)) / 0.1)
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(2.0, self._n)

    @property
    def solution(self):
        return np.array([-0.9, -0.95]), 34.3712389661618


class RotatedEllipse(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 7.0 * v[0] * v[0] - 6.0 * np.sqrt(3.0) * v[0] * v[1] + 13.0 * v[1] * v[1]

    @property
    def search_area(self):
        return create_symmetric_search_area(500.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Rump(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            (333.75 - v[0] * v[0]) * np.power(v[1], 6)
            + v[0]
            * v[0]
            * (
                11.0 * v[0] * v[0] * v[1] * v[1]
                - 121.0 * v[1] * v[1] * v[1] * v[1]
                - 2.0
            )
            + 5.5 * np.power(v[1], 8)
            + v[0] / (2.0 * v[1])
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(500.0, self._n)

    @property
    def solution(self):
        return np.array([0.0, 1e-17]), 0.0


class Salomon(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        p = np.square(v).sum()
        return 1.0 - np.cos(np.pi * np.sqrt(p)) + 0.1 * np.sqrt(p)

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Sargan(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        result = 0.0
        for i in range(self._n):
            temp_result = 0.0
            for j in range(self._n):
                if j != i:
                    temp_result += v[i] * v[j]
            result += v[i] * v[i] + 0.4 * temp_result
        return result

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class SchaffersFirst(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 0.5 + (
            np.square(np.sin(np.square(v[0] * v[0] + v[1] * v[1]))) - 0.5
        ) / np.square(1.0 + 0.001 * (v[0] * v[0] + v[1] * v[1]))

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class SchaffersSecond(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 0.5 + (
            np.square(np.sin(np.square(v[0] * v[0] - v[1] * v[1]))) - 0.5
        ) / np.square(1.0 + 0.001 * (v[0] * v[0] + v[1] * v[1]))

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class SchaffersThird(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return 0.5 + (
            np.square(np.sin(np.cos(np.abs(v[0] * v[0] - v[1] * v[1])))) - 0.5
        ) / np.square(1.0 + 0.001 * (v[0] * v[0] + v[1] * v[1]))

    @property
    def search_area(self):
        return create_symmetric_search_area(100.0, self._n)

    @property
    def solution(self):
        return np.array([0.0, 1.253114962205510]), 0.001566854526004


class Trecanni(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            v[0] * v[0] * v[0] * v[0] - 4 * v[0] * v[0] * v[0] + 4 * v[0] + v[1] * v[1]
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(5.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0


class Trid(create_fix_dim_function(6), OptimizationBenchmark):
    def call(self, v):
        p1 = np.square(v - 1.0).sum()
        p2 = np.sum(v[1:] * v[:-1])
        return p1 - p2

    @property
    def search_area(self):
        return create_symmetric_search_area(20.0, self._n)

    @property
    def solution(self):
        return np.array([6.0, 10.0, 12.0, 12.0, 10.0, 6.0]), -50.0


class Trefethen(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return (
            np.exp(np.sin(50.0 * v[0]))
            + np.sin(60.0 * np.exp(v[1]))
            + np.sin(70.0 * np.sin(v[0]))
            + np.sin(np.sin(80.0 * v[1]))
            - np.sin(10.0 * (v[0] + v[1]))
            + 0.25 * (v[0] * v[0] + v[1] * v[1])
        )

    @property
    def search_area(self):
        return create_symmetric_search_area(10.0, self._n)

    @property
    def solution(self):
        return np.array([-0.02440307923, 0.2106124261]), -3.3068686474752305


class Ursem(create_fix_dim_function(2), OptimizationBenchmark):
    def call(self, v):
        return -np.sin(2 * v[0] - 0.5 * np.pi) - 3.0 * np.cos(v[1]) - 0.5 * v[0]

    @property
    def search_area(self):
        return np.array([(-2.5, 3.0), (-2.0, 2.0)])

    @property
    def solution(self):
        return np.array([1.697136443570341, 0.0]), -4.816814063734823


class Zakharov(VariableDimFunction, OptimizationBenchmark):
    def call(self, v):
        p1 = np.square(v).sum()
        p2 = np.sum((np.arange(self._n) + 1) * v)
        return p1 + np.square(0.5 * p2) + np.power(0.5 * p2, 4)

    @property
    def search_area(self):
        return create_search_area(-5.0, 10.0, self._n)

    @property
    def solution(self):
        return create_solution_vector(0.0, self._n), 0.0
