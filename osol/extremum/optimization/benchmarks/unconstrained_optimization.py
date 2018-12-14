import numpy as np

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.optimization.benchmarks.optimization_benchmark import OptimizationBenchmark


class Ackley(OptimizationBenchmark):

    def __init__(self, n):
        self._n = n

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


class Alpine(OptimizationBenchmark):

    def __init__(self, n):
        self._n = n

    def call(self, v):
        v_ = v.to_numpy_array()
        return np.abs(v_ * np.sin(v_) + 0.1 * v_).sum()

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-10.0, 10.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 0.0


class Bartels_Conn(OptimizationBenchmark):

    def __init__(self):
        self._n = 2

    def call(self, v):
        return np.abs(v[0] * v[0] + v[1] * v[1] + v[0] * v[1]) + np.abs(np.sin(v[0])) + np.abs(np.cos(v[1]))

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-500.0, 500.0) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(**{f"x_{i + 1}": 0.0 for i in range(self._n)}), 1.0


class Beale(OptimizationBenchmark):

    def __init__(self):
        self._n = 2

    def call(self, v):
        return (1.5 - v[0] + v[0] * v[1]) * (1.5 - v[0] + v[0] * v[1]) + (2.25 - v[0] + v[0] * v[1] * v[1]) * (2.25 - v[0] + v[0] * v[1] * v[1]) + (2.625 - v[0] + v[0] * v[1] * v[1] * v[1]) * (2.625 - v[0] + v[0] * v[1] * v[1] * v[1])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-4.5, 4.5) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=3.0, x_2=0.5), 0.0


class Bird(OptimizationBenchmark):

    def __init__(self):
        self._n = 2

    def call(self, v):
        return np.sin(v[0]) * np.exp((1.0 - np.cos(v[1])) * (1.0 - np.cos(v[1]))) + np.cos(v[1]) * np.exp((1.0 - np.sin(v[0])) * (1.0 - np.sin(v[0]))) + (v[0] - v[1]) * (v[0] - v[1])

    @property
    def search_area(self):
        return {f"x_{i + 1}": (-4.5, 4.5) for i in range(self._n)}

    @property
    def solution(self):
        return Vector.create(x_1=4.70105575198105, x_2=3.152946019601391), -106.7645488423886


