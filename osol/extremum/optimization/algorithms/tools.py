from contracts import contract

import numpy as np

from osol.extremum.optimization.basic.vector import Vector


@contract
def generate_vector_in_box(area):
    """ Generates random vector uniformly distributed in rectangular area
        :param area: bounding box
        :type area: dict(str:tuple(number, number))
        :returns: random vector
        :rtype: vector
    """
    return Vector.create(values={k: np.random.uniform(left, right) for k, (left, right) in area.items()})


@contract
def generate_vector_in_sphere(current_point, radius, area=None):
    """ Generates random vector within a sphere built around the current one
        :param current_point: sphere center
        :type current_point: vector
        :param radius: sphere radius
        :type radius: number
        :param area: bounding box
        :type area: None|dict(str:tuple(number, number))
        :returns: random vector
        :rtype: vector
    """
    normally_distributed = Vector.create(values=dict(zip(area.keys(), np.random.normal(0.0, 1.0, len(area)))))
    shift = normally_distributed * (np.random.uniform(0.0, radius) / normally_distributed.length)
    moved_vector = current_point + shift
    if area:
        moved_vector = moved_vector.constrain(area=area)
    return moved_vector
