from contracts import contract

from osol.extremum.optimization.basic.algorithm import Algorithm
import osol.extremum.optimization.algorithms.tools as tools


class RandomSearch(Algorithm):
    """ Dummy version of random search

        State description:
            - `x`       =>     current best vector
            - `f_x`     =>     function value that corresponds to the current best vector
    """

    @contract
    def __init__(self, radius):
        """ Initialization of the algorithm

            :param radius: radius that is used to generate new points
            :type radius: number
        """
        self._radius = radius

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

        x_new = tools.generate_vector_in_sphere(x, self._radius, area=search_area)
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
