from osol.extremum.algorithm import OptimizationAlgorithm
from osol.extremum.tools.vectors import (
    bound_vector,
    generate_vector_in_area,
    generate_vector_in_sphere,
)


class RandomSearch(OptimizationAlgorithm):
    def __init__(self, radius):
        self.radius = radius

    def initialize(self, f, search_area):
        self.x = generate_vector_in_area(search_area)
        self.f_x = f(self.x)

    def iterate(self, f, search_area):
        x_new = generate_vector_in_sphere(self.x, self.radius)
        x_new = bound_vector(x_new, search_area)
        f_x_new = f(x_new)
        if f_x_new < self.f_x:
            self.x = x_new
            self.f_x = f_x_new

    def terminate(self, _, __):
        return self.x
