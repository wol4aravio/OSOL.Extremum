"""Set of tools for optimization algorithms."""


import numpy as np


def bound_vector(x, bounds):
    """Push vector to be located incide specified bounds."""
    return np.clip(x, a_min=bounds[:, 0], a_max=bounds[:, 1])
