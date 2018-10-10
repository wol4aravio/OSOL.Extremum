from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np
import math


def generate_random_point_in_rectangular(area):
    v = Vector({k: np.random.uniform(left, right) for k, (left, right) in area.items()})
    return v

def generate_random_point_in_sphere(current_point, radius, area):
    normally_distributed = Vector({k: v for k, v in zip(area.keys(), np.random.normal(0.0, 1.0, len(area)))})
    length = np.sqrt(sum(np.array(normally_distributed.values) ** 2))
    shift = (np.random.uniform(0.0, radius) / length) * normally_distributed
    return (current_point + shift).constrain(area)

def distance_between_vectors(v1, v2):
    return math.sqrt(sum(map(lambda v: v ** 2, (v2 - v1).values)))

def get_best_point_from_seed(seed, f):
    if isinstance(seed, list):
        point = sorted(seed, key=f)[0]
    else:
        point = seed
    return point
