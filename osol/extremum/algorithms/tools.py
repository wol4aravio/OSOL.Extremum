from contracts import contract

import numpy as np


@contract
def generate_vector_in_box(area):
    """ Generates random vector uniformly distributed in rectangular area
        :param area: bounding box
        :type area: list(tuple(number, number))
        :returns: random vector
        :rtype: array
    """
    return np.random.uniform(
        low=[l for (l, _) in area],
        high=[h for (_, h) in area])

@contract
def generate_vector_in_sphere(current_point, radius, area=None):
    """ Generates random vector within a sphere built around the current one
        :param current_point: sphere center
        :type current_point: array
        :param radius: sphere radius
        :type radius: number
        :param area: bounding box
        :type area: None|list(tuple(number, number))
        :returns: random array
        :rtype: array
    """
    normally_distributed = np.random.normal(0.0, 1.0, len(area))
    shift = normally_distributed * (np.random.uniform(0.0, radius) / np.linalg.norm(normally_distributed))
    moved_vector = current_point + shift
    if area:
        moved_vector = moved_vector.constrain(area=area)
    return moved_vector
