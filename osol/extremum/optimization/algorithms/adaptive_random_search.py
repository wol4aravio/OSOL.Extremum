from contracts import contract

from osol.extremum.optimization.basic.algorithm import Algorithm
import osol.extremum.optimization.algorithms.tools as tools


class AdaptiveRandomSearch(Algorithm):
    """ Adaptive random search

        State description:
            - `x`             =>     current best vector
            - `f_x`           =>     function value that corresponds to the current best vector
            - `r`             =>     current radius for point generation
            - `iter_id`       =>     current iteration number
            - `no_change`     =>     number of iterations without `x` modification
    """

    @contract
    def __init__(self, init_radius, factor_small, factor_huge, frequency, max_no_change):
        """ Initialization of the algorithm

            :param init_radius: initial radius for point generation
            :type init_radius: number

            :param factor_small: small coefficient for radius increase
            :type factor_small: number

            :param factor_huge: big coefficient for radius increase
            :type factor_huge: number

            :param frequency: radius increase frequency
            :type frequency: int

            :param max_no_change: max number of iterations without best point modification
            :type max_no_change: int
        """
        self._init_radius = init_radius
        self._factor_small = factor_small
        self._factor_huge = factor_huge
        self._frequency = frequency
        self._max_no_change = max_no_change

    def initialize(self, f, search_area, seed_state):
        initial_state = {}
        if seed_state is not None:
            raise NotImplementedError
        else:
            x = tools.generate_vector_in_box(search_area)
            initial_state["x"] = x
            initial_state["f_x"] = f(x)
            initial_state["r"] = self._init_radius
            initial_state["iter_id"] = 1
            initial_state["no_change"] = 0

        return initial_state

    def main_cycle(self, f, search_area, **kwargs):
        x = kwargs["x"]
        f_x = kwargs["f_x"]
        r = kwargs["r"]
        iter_id = kwargs["iter_id"]
        no_change = kwargs["no_change"]

        factor_small = self._factor_small
        factor_huge = self._factor_huge

        x_new_1 = tools.generate_vector_in_sphere(x, r, search_area)
        f_x_new_1 = f(x_new_1)

        if iter_id % self._frequency == 0:
            radius_huge = r * factor_huge
        else:
            radius_huge = r * factor_small

        x_new_2 = tools.generate_vector_in_sphere(x, radius_huge, search_area)
        f_x_new_2 = f(x_new_2)

        next_state = {
            "x": x,
            "f_x": f_x,
            "r": r,
            "iter_id": iter_id + 1,
            "no_change": no_change
        }

        if f_x_new_2 < f_x or f_x_new_1 < f_x:
            if f_x_new_2 < f_x_new_1:
                next_state["x"] = x_new_2
                next_state["f_x"] = f_x_new_2
                next_state["r"] = radius_huge
            else:
                next_state["x"] = x_new_1
                next_state["f_x"] = f_x_new_1
        else:
            next_state["no_change"] = no_change + 1
            if next_state["no_change"] > self._max_no_change:
                next_state["no_change"] = 0
                next_state["r"] /= factor_small

        return next_state

    def terminate(self, f, search_area, **kwargs):
        return kwargs["x"]
