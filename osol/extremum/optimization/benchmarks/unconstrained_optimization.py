import numpy as np

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.optimization.benchmarks.optimization_benchmark import OptimizationBenchmark


class VariableDimFunction:
    def __init__(self, n):
        self._n = n


def create_fix_dim_function(n):
    class FixDimFunction:
        def __init__(self):
            self._n = n
    return FixDimFunction


class Ackley(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        mean_pow = np.square(v_).mean()
        mean_cos = np.cos(2 * np.pi * v_).mean()
        return -20.0 * np.exp(-0.02 * np.sqrt(mean_pow)) - np.exp(mean_cos) + 20.0 + np.e

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-35.0, 35.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class Alpine(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return np.abs(v_ * np.sin(v_) + 0.1 * v_).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class BartelsConn(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return np.abs(v[0] * v[0] + v[1] * v[1] + v[0] * v[1]) + np.abs(np.sin(v[0])) + np.abs(np.cos(v[1]))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-500.0, 500.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 1.0


class Beale(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (1.5 - v[0] + v[0] * v[1]) * (1.5 - v[0] + v[0] * v[1]) + (2.25 - v[0] + v[0] * v[1] * v[1]) * (2.25 - v[0] + v[0] * v[1] * v[1]) + (2.625 - v[0] + v[0] * v[1] * v[1] * v[1]) * (2.625 - v[0] + v[0] * v[1] * v[1] * v[1])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-4.5, 4.5) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=3.0, x_2=0.5), 0.0


class Bird(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return np.sin(v[0]) * np.exp((1.0 - np.cos(v[1])) * (1.0 - np.cos(v[1]))) + np.cos(v[1]) * np.exp((1.0 - np.sin(v[0])) * (1.0 - np.sin(v[0]))) + (v[0] - v[1]) * (v[0] - v[1])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-2.0 * np.pi, 2.0 * np.pi) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=4.70105575198105, x_2=3.152946019601391), -106.7645488423886


class Bohachevsky(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return v[0] * v[0] + 2 * v[1] * v[1] - 0.3 * np.cos(3.0 * np.pi * v[0]) - 0.4 * np.cos(4 * np.pi * v[1]) + 0.7

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-100.0, 100.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=0.0), 0.0


class Booth(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (v[0] + 2.0 * v[1] - 7.0) * (v[0] + 2.0 * v[1] - 7.0) + (2.0 * v[0] + v[1] - 5.0) * (2.0 * v[0] + v[1] - 5.0)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=1.0, x_2=3.0), 0.0


class BoxBettsQuadraticSum(create_fix_dim_function(3), OptimizationBenchmark):

    def g(self, i, v):
        return np.exp(-0.1 * (i + 1) * v[0]) - np.exp(-0.1 * (i + 1) * v[1]) - (np.exp(-0.1 * (i + 1)) - np.exp(-(i + 1)) * v[2])

    def call(self, v):
        D = 10
        temp = np.array([self.g(i, v) for i in range(D)])
        return np.square(temp).sum()

    @property
    def search_area(self):
        return {
            "x_1": (0.9, 1.2),
            "x_2": (9.0, 11.2),
            "x_3": (0.9, 1.2)
        }

    @property
    def solution(self):
        return Vector.create(x_1=1.0, x_2=10.0, x_3=1.0), 0.0


class BraninRCOS(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (v[1] - 5.1 * v[0] * v[0] / (4 * np.pi * np.pi) + 5 * v[0] / np.pi - 6) * (v[1] - 5.1 * v[0] * v[0] / (4 * np.pi * np.pi) + 5 * v[0] / np.pi - 6) + 10.0 * (1.0 - 1.0 / (8.0 * np.pi)) * np.cos(v[0]) + 10.0

    @property
    def search_area(self):
        return {
            "x_1": (-5.0, 10.0),
            "x_2": (0.0, 15.0)
        }

    @property
    def solution(self):
        return Vector.create(x_1=-np.pi, x_2=12.275), 0.39788735772973816


class Brent(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (v[0] + 10.0) * (v[0] + 10.0) + (v[1] + 10.0) * (v[1] + 10.0) + np.exp(-v[0] * v[0] - v[1] * v[1])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=-10.0, x_2=-10.0), 0.0


class Brown(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v1_ = v.to_numpy_array()[:-1]
        v2_ = v.to_numpy_array()[1:]
        return np.sum(np.power(np.square(v1_), v2_ * v2_ + 1.0) + np.power(np.square(v2_), v1_ * v1_ + 1.0))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 4.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class Bukin(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 100 * v[1] ** 2 + 0.01 * np.abs(v[0] + 10)

    @property
    def search_area(self):
        return {
            "x_1": (-15.0, -5.0),
            "x_2": (-3.0, 3.0)
        }

    @property
    def solution(self):
        return Vector.create(x_1=-10.0, x_2=0.0), 0.0


class CamelThreeHumps(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 2.0 * v[0] * v[0] - 1.05 * v[0] * v[0] * v[0] * v[0] + v[0] * v[0] * v[0] * v[0] * v[0] * v[0] / 6.0 + v[0] * v[1] + v[1] * v[1]

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-5.0, 5.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class Chichinadze(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return v[0] * v[0] - 12.0 * v[0] + 11.0 + 10.0 * np.cos(np.pi * v[0] / 2.0) + 8.0 * np.sin(5.0 * np.pi * v[0] / 2.0) - np.sqrt(0.2) * np.exp(-0.5 * (v[1] - 0.5) * (v[1] - 0.5))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-30.0, 30.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=6.1898665869658, x_2=0.5), -42.94438552656265


class Colville(create_fix_dim_function(4), OptimizationBenchmark):

    def call(self, v):
        return 100.0 * (v[0] - v[1] * v[1]) * (v[0] - v[1] * v[1]) + (1.0 - v[0]) * (1.0 - v[0]) + 90.0 * (v[3] - v[2] * v[2]) * (v[3] - v[2] * v[2]) + (1.0 - v[2]) * (1.0 - v[2]) + 10.1 * ((v[1] - 1.0) * (v[1] - 1.0) + (v[3] - 1.0) * (v[3] - 1.0)) + 19.8 * (v[1] - 1.0) * (v[3] - 1.0)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 1.0 for i in range(self._n)}), 0.0


class Corana(create_fix_dim_function(4), OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        d = np.array([1.0, 1000.0, 10.0, 100.0])
        z = 0.2 * (np.abs(v_ / 0.2) + 0.49999) * np.sign(v_)
        v = np.abs(v_ - z)
        A = 0.05
        part_1 = (np.abs(v) < A) * (0.15 * (z - 0.05 * np.sign(z)) * (z - 0.05 * np.sign(z)) * d)
        part_2 = (np.abs(v) >= A) * (d * np.square(v_))
        return np.sum(part_1 + part_2)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-500.0, 500.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class CosineMixture(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return np.sum(-(0.1 * np.cos(5.0 * np.pi * v_) - v_ * v_))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), -0.1 * self._n


class Csendes(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return (np.power(v_, 6.0) * (2.0 + np.sin(1.0 / v_))).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 1e-9 for i in range(self._n)}), 0.0


class Cube(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 100.0 * (v[1] - v[0] * v[0] * v[0]) * (v[1] - v[0] * v[0] * v[0]) + (1.0 - v[0]) * (1.0 - v[0])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 1.0 for i in range(self._n)}), 0.0


class Damavandi(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (1.0 - np.power(np.abs(((np.sin(np.pi * (v[0] - 2))) * np.sin(np.pi * (v[0] - 2))) / (np.pi * np.pi * (v[0] - 2.0) * (v[1] - 2.0))), 5)) * (2.0 + (v[0] - 7.0) * (v[0] - 7.0) + 2.0 * (v[1] - 7.0) * (v[1] - 7.0))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (0.0, 14.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": (2.0 + 1e-5) for i in range(self._n)}), 0.0


class Deb(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return (-np.power(np.sin(5.0 * np.pi * v_), 6.0) / self._n).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": -0.9 for i in range(self._n)}), -1.0


class DeckkersAarts(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 100000.0 * v[0] * v[0] + v[1] * v[1] - (v[0] * v[0] + v[1] * v[1]) * (v[0] * v[0] + v[1] * v[1]) + 0.00001 * np.power(v[0] * v[0] + v[1] * v[1], 4)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-20.0, 20.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=15.0), -24771.09375


class DixonAndPrice(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v1 = v.to_numpy_array()[1:]
        v2 = v.to_numpy_array()[:-1]
        return (v[0] - 1.0) * (v[0] - 1.0) + (np.arange(2, self._n + 1) * np.square(2.0 * np.square(v1) - v2)).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": np.power(2.0, -(np.power(2.0, i + 1) - 2.0) / np.power(2.0, i + 1)) for i in range(self._n)}), 0.0


class Dolan(create_fix_dim_function(5), OptimizationBenchmark):

    def call(self, v):
        return (v[0] + 1.7 * v[1]) * np.sin(v[0]) - 1.5 * v[2] - 0.1 * v[3] * np.cos(v[4] + v[3] - v[0]) + 0.2 * v[4] * v[4] - v[1] - 1.0

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-100.0, 100.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=98.964258312237106, x_2=100, x_3=100, x_4=99.224323672554704, x_5=-0.249987527588471), -529.8714413460193


class Easom(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return -np.cos(v[0]) * np.cos(v[1]) * np.exp(-(v[0] - np.pi) * (v[0] - np.pi) - (v[1] - np.pi) * (v[1] - np.pi))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-100.0, 100.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=np.pi, x_2=np.pi), -1.0


class EggCrate(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return v[0] * v[0] + v[1] * v[1] + 25.0 * (np.sin(v[0]) * np.sin(v[0]) + np.sin(v[1]) * np.sin(v[1]))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-5.0, 5.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=0.0), 0.0


class EggHolder(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return -(v[1] + 47.0) * np.sin(np.sqrt(np.abs(v[1] + v[0] / 2.0 + 47.0))) - v[0] * np.sin(np.sqrt(np.abs(v[0] - (v[1] + 47.0))))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-512.0, 512.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=512.0, x_2=404.2319), -959.640662709941


class Exponential(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return -np.exp((-0.5 * np.square(v_)).sum())

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), -1.0


class Goldstein(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (1.0 + (v[0] + v[1] + 1.0) * (v[0] + v[1] + 1.0) * (19.0 - 14.0 * v[0] + 3.0 * v[0] * v[0] - 14.0 * v[1] + 6.0 * v[0] * v[1] + 3.0 * v[1] * v[1])) * (30.0 + (2.0 * v[0] - 3 * v[1]) * (2.0 * v[0] - 3 * v[1]) * (18.0 - 32.0 * v[0] + 12.0 * v[0] * v[0] + 48.0 * v[1] - 36 * v[0] * v[1] + 27.0 * v[1] * v[1]))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-2.0, 2.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=-1.0), 3.0


class Griewank(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return 1.0 + np.sum((np.square(v_) / 4000.0)) - np.prod(np.cos(v_ / np.sqrt(1 + np.arange(self._n))))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-100.0, 100.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class GulfResearch(create_fix_dim_function(3), OptimizationBenchmark):

    def call(self, v):
        i = np.arange(1, 100)
        u = 25.0 + np.power(-50.0 * np.log(0.01 * i), 1.0 / 1.5)
        return np.square(np.exp(-np.power(u - v[1], v[2]) / v[0]) - 0.01 * i).sum()

    @property
    def search_area(self):
        return {
            "x_1": (0.1, 100.0),
            "x_2": (0.0, 25.6),
            "x_3": (0.0, 5.0)
        }

    @property
    def solution(self):
        return Vector.create(x_1=50.0, x_2=25.0, x_3=1.5), 0.0


class Hansen(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        i = np.arange(5)
        p1 = (i + 1) * np.cos(i * v[0] + i + 1.0)
        p2 = (i + 1) * np.cos((i + 2) * v[1] + i + 1.0)
        return p1.sum() * p2.sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=-7.58989583, x_2=-7.70831466), -176.54179313664181


class HelicalValley(create_fix_dim_function(3), OptimizationBenchmark):

    def call(self, v):
        if v[0] >= 0.0:
            theta = np.arctan(v[1] / v[0]) / (2.0 * np.pi)
        else:
            theta = (np.pi + np.arctan(v[1] / v[0])) / (2.0 * np.pi)
        return 100.0 * (np.square(v[2] - 10.0 * theta) + np.square(np.sqrt(v[0] * v[0] + v[1] * v[1]) - 1.0)) + v[2] * v[2]

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-100.0, 100.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=1.0, x_2=0.0000000001, x_3=0.0), 0.0


class Himmelblau(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return np.square(v[0] * v[0] + v[1] - 11.0) + np.square(v[0] + v[1] * v[1] - 7.0)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-5.0, 5.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=3.0, x_2=2.0), 0.0


class Hosaki(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (1.0 - 8.0 * v[0] + 7 * v[0] * v[0] - 7.0 * v[0] * v[0] * v[0] / 3.0 + 0.25 * v[0] * v[0] * v[0] * v[0]) * v[1] * v[1] * np.exp(-v[1])

    @property
    def search_area(self):
        return {
            "x_1": (0.0, 5.0),
            "x_2": (0.0, 6.0)
        }

    @property
    def solution(self):
        return Vector.create(x_1=4.0, x_2=2.0), -2.3458115458488518


class JennrichSampson(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        i = np.arange(1, 11)
        return np.square(2.0 + 2.0 * i - (np.exp(i * v[0]) + np.exp(i * v[1]))).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.257825, x_2=0.257825), 124.36218236258078


class Keane(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return np.square(np.sin(v[0] - v[1]) * np.sin(v[0] + v[1])) / np.sqrt(v[0] * v[0] + v[1] * v[1])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (0.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=1.39325), 0.6736675


class Langermann(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        a = np.array([9.681, 9.4, 8.025, 2.196, 8.074])
        b = np.array([0.667, 2.041, 9.152, 0.415, 8.777])
        c = np.array([0.806, 0.517, 0.1, 0.908, 0.965])
        result = c * np.cos(np.pi * ((v[0] - a) * (v[0] - a) + (v[1] - b) * (v[1] - b))) / np.exp(((v[0] - a) * (v[0] - a) + (v[1] - b) * (v[1] - b)) / np.pi)
        return np.sum(-result)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (0.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=9.6810707, x_2=0.6666515), -1.08093846723926811925764468469


class Leon(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 100.0 * (v[1] - v[0] * v[0]) * (v[1] - v[0] * v[0]) + (1.0 - v[0]) * (1.0 - v[0])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.2, 1.2) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=1.0, x_2=1.0), 0.0


class Matyas(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 0.26 * (v[0] * v[0] + v[1] * v[1]) - 0.48 * v[0] * v[1]

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=0.0), 0.0


class McCormick(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return np.sin(v[0] + v[1]) + (v[0] - v[1]) * (v[0] - v[1]) - v[0] + 2.0 * v[1] + 1.0

    @property
    def search_area(self):
        return {
            "x_1": (-1.5, 4.0),
            "x_2": (-3.0, 3.0)
        }

    @property
    def solution(self):
        return Vector.create(x_1=-0.5471975602214493, x_2=-1.547197559268372), -1.413222955457575


class MieleCantrell(create_fix_dim_function(4), OptimizationBenchmark):

    def call(self, v):
        return np.power(np.exp(-v[0]) - v[1], 4) + 100.0 * np.power(v[1] - v[2], 6) + np.power(np.tan(v[2] - v[3]), 4) + np.power(v[0], 8)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-1.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=1.0, x_3=1.0, x_4=1.0), 0.0


class MishraZeroSum(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return 100.0 * np.sqrt(np.abs(v_.sum()))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class Parsopoulos(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return np.square(np.cos(v[0])) + np.square(np.sin(v[1]))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-5.0, 5.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=np.pi/2.0, x_2=0.0), 0.0


class PenHolder(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return -np.exp(-1.0 / np.abs(np.cos(v[0]) * np.cos(v[1]) * np.exp(np.abs(1.0 - np.sqrt(v[0] * v[0] + v[1] * v[1]) / np.pi))))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-11.0, 11.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=9.646167671043401, x_2=9.646167671043401), -0.9635348327265058


class Pathological(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v1 = v.to_numpy_array()[:-1]
        v2 = v.to_numpy_array()[1:]
        return np.sum(0.5 + (np.square(np.sin(np.sqrt(100.0 * v1 * v1 + v2 * v2))) - 0.5) / (1.0 + 0.001 * np.square(v1 * v1 - 2 * v1 * v2 + v2 * v2)))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-100.0, 100.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class Paviani(create_fix_dim_function(10), OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        p1 = np.sum(np.square(np.log(v_ - 2.0)) + np.square(np.log(10.0 - v_)))
        p2 = np.prod(v_)
        return p1 - np.power(p2, 0.2)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (2.0001, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 9.351 for i in range(self._n)}), -45.778451456928394


class Periodic(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 1.0 + np.square(np.sin(v[0])) + np.square(np.sin(v[1])) - 0.1 * np.exp(-(v[0] * v[0] + v[1] * v[1]))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.0, x_2=0.0), 0.9


class Price(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return (np.abs(v[0]) - 5.0) * (np.abs(v[0]) - 5.0) + (np.abs(v[1]) - 5.0) * (np.abs(v[1]) - 5.0)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-500.0, 500.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=5.0, x_2=5.0), 0.0


class Quadratic(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return -3803.84 - 138.08 * v[0] - 232.92 * v[1] + 128.08 * v[0] * v[0] + 203.64 * v[1] * v[1] + 182.25 * v[0] * v[1]

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=0.19388, x_2=0.48513), -3873.724182183056


class Quintic(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return np.abs(np.power(v_, 5) - 3.0 * np.power(v_, 4) + 4.0 * np.power(v_, 3) + 2.0 * np.square(v_) - 10.0 * v_ - 4.0)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": -1.0 for i in range(self._n)}), 0.0


class Ripple(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v_ = v.to_numpy_array()
        return -(np.exp(-2 * np.log(2) * np.square((v_ - 0.1) / 0.8)) * (np.power(np.sin(5.0 * np.pi * v_), 6) + 0.1 * np.square(np.cos(500.0 * np.pi * v_)))).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (0.0, 1.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.1 for i in range(self._n)}), -self._n * 1.1


class Rosenbrock(VariableDimFunction, OptimizationBenchmark):

    def call(self, v):
        v1 = v.to_numpy_array()[1:]
        v2 = v.to_numpy_array()[:-1]
        return (100.0 * (v1 - v2 * v2) * (v1 - v2 * v2) + (v2 - 1.0) * (v2 - 1.0)).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-30.0, 30.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 1.0 for i in range(self._n)}), 0.0


class RosenbrockModified(create_fix_dim_function(2), OptimizationBenchmark):

    def call(self, v):
        return 74.0 + 100.0 * (v[1] - v[0] * v[0]) * (v[1] - v[0] * v[0]) + (1.0 - v[0]) * (1.0 - v[0]) - 400.0 * np.exp(-((v[0] + 1) * (v[0] + 1) + (v[1] + 1) * (v[1] + 1)) / 0.1)

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-2.0, 2.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=-0.9, x_2=-0.95), 34.37125655899683
