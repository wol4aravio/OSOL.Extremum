"""Description of Gradient Descent (GD) algorithm."""

import random

import numpy as np
import numpy.linalg as la
from osol.algorithms.template import AlgorithmFirstOrder
from osol.algorithms.tools import bound_vector


class GradientDescent(AlgorithmFirstOrder):
    """GD implementation."""

    def __init__(self, eps):
        """Class constructor."""
        self.eps = eps
        self.x = None

        self._n_dim = None

    def initialize(self, f, f_grad, search_area):
        self._n_dim = search_area.shape[0]

        self.x = np.zeros(search_area.shape[0])
        for i in range(self._n_dim):
            self.x[i] = random.uniform(search_area[i, 0], search_area[i, 1])
        self.y = f(self.x)

    def iterate(self, f, f_grad, search_area):
        grad = f_grad(self.x)
        x_new = self.x - random.uniform(0.0, self.eps) * grad / la.norm(grad)
        x_new = bound_vector(x_new, search_area)
        y_new = f(x_new)
        if y_new < self.y:
            self.x = x_new
            self.y = y_new

    def terminate(self, f, f_grad, search_area):
        return self.x
