from contracts import contract

import numpy as np

from osol.extremum.algorithms.algorithm import Algorithm
import osol.extremum.algorithms.tools as tools


class LuusJaakolaOptimization(Algorithm):
    """ Modified Luus-Jaakola Optimization Algorithm

        State description:
            - `x`             =>     current best vector
            - `f_x`           =>     function value that corresponds to the current best vector
            - `r`             =>     current radius for point generation
            - `run_id`        =>     current run number
            - `iter_id`       =>     current iteration number
    """

    @contract
    def __init__(self, init_radius, number_of_samples, reduction_coefficient, recover_coefficient, iteration_per_run):
        """ Initialization of the algorithm

            :param init_radius: initial radius for point generation
            :type init_radius: number

            :param number_of_samples: number of samples to be generated
            :type number_of_samples: int

            :param reduction_coefficient: radius reduction coefficient
            :type reduction_coefficient: number

            :param recover_coefficient: radius initialization coefficient for runs
            :type recover_coefficient: number

            :param iteration_per_run: number of iterations before radius modification
            :type iteration_per_run: int

        """
        self._init_radius = init_radius
        self._number_of_samples = number_of_samples
        self._reduction_coefficient = reduction_coefficient
        self._recover_coefficient = recover_coefficient
        self._iteration_per_run = iteration_per_run

    def initialize(self, f, search_area, seed_state):
        initial_state = {}
        if seed_state is not None:
            raise NotImplementedError
        else:
            x = tools.generate_vector_in_box(search_area)
            initial_state["x"] = x
            initial_state["f_x"] = f(x)
            initial_state["r"] = self._set_radius(0)
            initial_state["run_id"] = 0
            initial_state["iter_id"] = 0

        return initial_state

    def _set_radius(self, run_id):
        return np.power(self._recover_coefficient, run_id) * self._init_radius

    def main_cycle(self, f, search_area, **kwargs):
        x = kwargs["x"]
        f_x = kwargs["f_x"]
        r = kwargs["r"]
        iter_id = kwargs["iter_id"]
        run_id = kwargs["run_id"]
        N = self._number_of_samples

        x_new = x.copy()
        f_x_new = f_x

        for _ in range(N):
            _x = tools.generate_vector_in_sphere(x_new, r, search_area)
            _f_x = f(_x)

            if _f_x < f_x_new:
                x_new = _x
                f_x_new = _f_x

        r_new = r * self._reduction_coefficient
        run_id_new = run_id
        iter_id_new = iter_id + 1

        if iter_id_new == self._iteration_per_run:
            iter_id_new = 0
            run_id_new = run_id + 1
            r_new = self._set_radius(run_id_new)

        return {
            "x": x_new,
            "f_x": f_x_new,
            "r": r_new,
            "iter_id": iter_id_new,
            "run_id": run_id_new
        }

    def terminate(self, f, search_area, **kwargs):
        return kwargs["x"]
