from Numerical_Objects.Vector import Vector

import numpy as np


def generate_random_point_in_sphere(current_point, radius, area):
    normally_distributed = Vector({k: v for k, v in zip(area.keys(), np.random.normal(0.0, 1.0, len(area)))})
    length = np.sqrt(sum(np.array(normally_distributed.values) ** 2))
    shift = (np.random.uniform(0.0, radius) / length) * normally_distributed
    return (current_point + shift).constrain(area)
