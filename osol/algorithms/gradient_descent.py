"""Description of Gradient Descent (GD) algorithm."""

import random

import numpy.linalg as la
from osol.algorithms.template import AlgorithmFirstOrder
from osol.algorithms.tools import bound_vector, generate_point_in_area


class GradientDescent(AlgorithmFirstOrder):
    """GD implementation."""

    def __init__(self, eps):
        """Class constructor."""
        self.eps = eps
        self.x = None

    def initialize(self, f, f_grad, search_area):
        self.x = generate_point_in_area(search_area)
        self.y = f(self.x)

    def iterate(self, f, f_grad, search_area):
        grad = f_grad(self.x)
        grad_norm = grad / la.norm(grad)
        x_new = self.x - random.uniform(0.0, self.eps) * grad_norm
        x_new = bound_vector(x_new, search_area)
        y_new = f(x_new)
        if y_new < self.y:
            self.x = x_new
            self.y = y_new

    def terminate(self, f, f_grad, search_area):
        return self.x
