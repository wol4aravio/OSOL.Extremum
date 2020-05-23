"""Description of Random Search (RS) algorithm."""

import numpy as np
import numpy.linalg as la
from osol.algorithms.template import AlgorithmZeroOrder
from osol.algorithms.tools import bound_vector, generate_point_in_area


class RandomSearch(AlgorithmZeroOrder):
    """RS implementation."""

    def __init__(self, eps):
        """Class constructor."""
        self.eps = eps
        self.x = None
        self._n_dim = None

    def _generate_point(self, x_0, search_area):
        delta = np.random.uniform(low=-1.0, high=1.0, size=(self._n_dim),)
        delta = delta / la.norm(delta)
        x_1 = x_0 + self.eps * delta
        x_1 = bound_vector(x_1, search_area)
        return x_1

    def initialize(self, f, search_area):
        self._n_dim = search_area.shape[0]
        self.x = generate_point_in_area(search_area)
        self.y = f(self.x)

    def iterate(self, f, search_area):
        x_new = self._generate_point(self.x, search_area)
        y_new = f(x_new)
        if y_new < self.y:
            self.x = x_new
            self.y = y_new

    def terminate(self, f, search_area):
        return self.x
