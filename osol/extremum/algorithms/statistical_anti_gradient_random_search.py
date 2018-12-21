from contracts import contract

import numpy as np

from osol.extremum.algorithms.algorithm import Algorithm
import osol.extremum.algorithms.tools as tools


class StatisticalAntiGradientRandomSearch(Algorithm):
    """ Random search with statistical anti gradient

        State description:
            - `x`       =>     current best vector
            - `f_x`     =>     function value that corresponds to the current best vector
    """

    @contract
    def __init__(self, radius, number_of_samples):
        """ Initialization of the algorithm

            :param radius: radius that is used to generate new points
            :type radius: number

            :param number_of_samples: number of samples to be generated
            :type number_of_samples: int
        """
        self._radius = radius
        self._number_of_samples = number_of_samples

    def initialize(self, f, search_area, seed_state):
        initial_state = {}
        if seed_state is not None:
            raise NotImplementedError
        else:
            x = tools.generate_vector_in_box(search_area)
            initial_state["x"] = x
            initial_state["f_x"] = f(x)

        return initial_state

    def main_cycle(self, f, search_area, **kwargs):
        x = kwargs["x"]
        f_x = kwargs["f_x"]

        r = self._radius
        N = self._number_of_samples

        new_points = [tools.generate_vector_in_sphere(x, r, search_area) for _ in range(N)]
        new_values = [f(p) for p in new_points]

        anti_gradient = np.zeros(shape=len(search_area))
        for point, f_point in zip(new_points, new_values):
            anti_gradient -= (point - x) * (f_point - f_x)
        anti_grad_length = anti_gradient.length
        if anti_grad_length > 0.0:
            anti_gradient *= 1.0 / anti_grad_length

        x_new = tools.constrain(x + anti_gradient * np.random.uniform(0.0, r), search_area)
        f_x_new = f(x_new)

        if f_x_new < f_x:
            return {
                "x": x_new,
                "f_x": f_x_new
            }
        else:
            return {
                "x": x,
                "f_x": f_x
            }

    def terminate(self, f, search_area, **kwargs):
        return kwargs["x"]
