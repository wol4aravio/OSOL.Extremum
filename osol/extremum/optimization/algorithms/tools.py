from contracts import contract

import numpy as np

from osol.extremum.optimization.basic.vector import Vector


@contract
def generate_vector(area):
    """ Generates random vector uniformly distributed in rectangular area

        :param area: bounding box
        :type area: dict(str:tuple(number, number))

        :returns: random vector
        :rtype: vector
    """
    return Vector.create(**{k: np.random.uniform(left, right) for k, (left, right) in area.items()})
