"""Set of tools for optimization algorithms."""


import random

import numpy as np


def bound_vector(x, bounds):
    """Push vector to be located incide specified bounds."""
    return np.clip(x, a_min=bounds[:, 0], a_max=bounds[:, 1])


def generate_point_in_area(area):
    """Generate point within area."""
    x = np.zeros(area.shape[0])
    for i in range(len(x)):
        x[i] = random.uniform(area[i, 0], area[i, 1])
    return x
