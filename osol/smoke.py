"""Tools for generation of functions for smoke tests."""

import numpy as np


def generate_smoke_L2(n_dim, bounds=(-10, 10)):
    """
    Generate smoke function:
    f(x) = sum(((x - x_sol)^T * (x - x_sol)) ** 2)
    """
    x_solution = np.random.uniform(
        low=bounds[0], high=bounds[1], size=(n_dim),
    )

    def f(x):
        return np.sum((x - x_solution) ** 2)

    f.solution = x_solution
    f.search_area = np.full(shape=(n_dim, 2), fill_value=bounds)
    return f