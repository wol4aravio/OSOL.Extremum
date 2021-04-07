import numpy as np

from osol.algorithms.abstract import OptimizationAlgorithm
from osol.tools.vectors import bound_vector, generate_vector_in_area


class BigBangBigCrunch(OptimizationAlgorithm):
    def __init__(self, N, radius):
        self.N = N
        self.radius = radius

    def _calculate_values(self, f):
        self.values = [f(x) for x in self.points]

    def _get_center_of_mass(self):
        return self.points[np.where(self.values == np.min(self.values))[0][0]]

    def _generate_delta(self, x):
        return self.radius * np.random.normal(size=x.size) / self.iteration_number

    def initialize(self, f, search_area):
        self.iteration_number = 1
        self.points = [generate_vector_in_area(search_area) for _ in range(self.N)]
        self._calculate_values(f)

    def iterate(self, f, search_area):
        center_of_mass = self._get_center_of_mass()

        self.points = [center_of_mass + self._generate_delta(x) for x in self.points]
        self.points = [bound_vector(x, search_area) for x in self.points]
        self.points.append(center_of_mass)
        self._calculate_values(f)

        self.iteration_number += 1

    def terminate(self, _, __):
        return self._get_center_of_mass()
