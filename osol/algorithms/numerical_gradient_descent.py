import numpy as np
from scipy.optimize import approx_fprime

from osol.algorithms.abstract import OptimizationAlgorithm
from osol.tools.vectors import bound_vector, generate_vector_in_area


class NumericalGradientDescent(OptimizationAlgorithm):
    def __init__(self, radius, eps=1e-7):
        self.radius = radius
        self.eps = eps

    def initialize(self, f, search_area):
        self.x = generate_vector_in_area(search_area)
        self.f_x = f(self.x)

    def iterate(self, f, search_area):
        gradient = approx_fprime(self.x, f, epsilon=self.eps)
        gradient_length = np.linalg.norm(gradient)
        if gradient_length > 0:
            gradient /= gradient_length

        x_new = self.x - np.random.uniform(0.0, self.radius) * gradient
        x_new = bound_vector(x_new, search_area)
        f_x_new = f(x_new)
        if f_x_new < self.f_x:
            self.x = x_new
            self.f_x = f_x_new

    def terminate(self, _, __):
        return self.x
