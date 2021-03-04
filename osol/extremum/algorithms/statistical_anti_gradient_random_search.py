import numpy as np

from osol.extremum.algorithm import OptimizationAlgorithm
from osol.extremum.tools.vectors import (
    bound_vector,
    generate_vector_in_area,
    generate_vector_in_sphere,
)


class StatisticalAntiGradientRandomSearch(OptimizationAlgorithm):
    def __init__(self, radius, number_of_samples):
        self.radius = radius
        self.number_of_samples = number_of_samples

    def initialize(self, f, search_area):
        self.x = generate_vector_in_area(search_area)
        self.f_x = f(self.x)

    def iterate(self, f, search_area):
        antigrad_x = [
            generate_vector_in_sphere(self.x, self.radius)
            for _ in range(self.number_of_samples)
        ]
        antigrad_f_x = [f(x) for x in antigrad_x]

        anti_gradient = np.zeros(shape=len(search_area))
        for temp_x, temp_f_x in zip(antigrad_x, antigrad_f_x):
            anti_gradient -= (temp_x - self.x) * (temp_f_x - self.f_x)
        anti_gradient_length = np.linalg.norm(anti_gradient)
        if anti_gradient_length > 0:
            anti_gradient /= anti_gradient_length

        x_new = self.x + np.random.uniform(0.0, self.radius) * anti_gradient
        x_new = bound_vector(x_new, search_area)
        f_x_new = f(x_new)
        if f_x_new < self.f_x:
            self.x = x_new
            self.f_x = f_x_new

    def terminate(self, _, __):
        return self.x
