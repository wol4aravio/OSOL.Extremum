"""Set of tools for optimization algorithms."""

import numpy as np


def bound_vector(x, bounds):
    """Push vector to be located incide specified bounds."""
    return np.clip(x, a_min=bounds[:, 0], a_max=bounds[:, 1])


def generate_point_in_area(area):
    """Generate point within area."""
    left, right = area[:, 0], area[:, 1]
    return left + np.random.rand(area.shape[0]) * (right - left)
