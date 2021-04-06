# pylint: disable=protected-access

import numpy as np


class FeldbaumTestFunctions:
    @staticmethod
    def _generate_function(a, b, c, p):
        return lambda x: np.sum(a * np.abs(x - c) ** p) + b

    def _compose_function_parts(self):
        self._functions = [
            FeldbaumTestFunctions._generate_function(
                self._a[i, :], self._b[i, :], self._c[i, :], self._p[i, :]
            )
            for i in range(self._N)
        ]

    def __init__(self, N, dim):
        self._N = N
        self._dim = dim
        self._a = np.random.uniform(low=0.0, high=5.0, size=(N, dim))
        self._b = np.random.uniform(low=-10.0, high=10.0, size=(N, 1))
        self._c = np.random.uniform(low=-10.0, high=10.0, size=(N, dim))
        self._p = np.random.uniform(low=0.0, high=5.0, size=(N, dim))
        self._functions = None
        self._compose_function_parts()

    def __call__(self, x):
        return np.min([f(x) for f in self._functions])


def smoke_check(algorithm, number_of_iterations, eps=1e-2):
    left, right = -10, 10
    search_area = np.array([[left, right], [left, right]])
    x_opt = np.random.uniform(left, right, 2)
    x_found = algorithm.optimize(
        lambda x: np.sum((x - x_opt) ** 2), search_area, number_of_iterations
    )
    return np.linalg.norm(x_found - x_opt) < eps


def feldbaum_check(algorithm, number_of_iterations, eps=1e-2):
    left, right = -10, 10
    search_area = np.array([[left, right], [left, right]])
    f = FeldbaumTestFunctions(N=3, dim=2)
    y_opt = np.min(f._b)
    y_opt_loc = np.where(f._b == y_opt)[0][0]
    x_opt = f._c[y_opt_loc, :]
    x_found = algorithm.optimize(f, search_area, number_of_iterations)
    return np.linalg.norm(x_found - x_opt) < eps
