from contracts import contract
import numpy as np

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.optimization.basic.algorithm import Algorithm
import osol.extremum.optimization.algorithms.tools as tools

from osol.extremum.etc.new_contracts import * # Inclusion of user defined contracts


class BigBangBigCrunch(Algorithm):
    """ Big Bang Big Crunch Algorithm

        State description:
            - `points`             =>     set of current points
            - `points_quality`     =>     quality for the `points`
            - `best_value`         =>     best value of objective function that was observed
            - `iter_id`            =>     current iteration id
    """

    @contract
    def __init__(self, number_of_points, scatter_parameter):
        """ Initialization of the algorithm

            :param number_of_points: number of points to be processed
            :type number_of_points: int

            :param scatter_parameter: affects area for new point generation
            :type scatter_parameter: number
        """
        self._number_of_points = number_of_points
        self._scatter_parameter = scatter_parameter

    @staticmethod
    @contract
    def get_quality(points, best_value, f):
        """ Calculates point quality

            :param points: points to be evaluated
            :type points: list[N](Vector)

            :param best_value: previously observed best value
            :type best_value: number

            :param f: objective function
            :type f: Function

            :returns: quality of the observed points
            :rtype: tuple(list[N](number), number)
        """
        point_values = [f(p) for p in points]
        best_point_value = min(point_values)
        new_best_value = min(best_value, best_point_value)
        point_quality = [(v - new_best_value + 1e-7) for v in point_values]
        return point_quality, new_best_value

    @staticmethod
    @contract
    def big_crunch(points, points_quality):
        """ Big Crunch procedure

            :param points: points to be evaluated
            :type points: list[N](Vector)

            :param points_quality: quality of the observed points
            :type points_quality: list[N](number)

            :returns: center of mass
            :rtype: Vector
        """
        center = Vector(values=np.zeros(shape=points[0].ndim), keys=points[0].keys())
        for p, q in zip(points, points_quality):
            center += p / q
        center /= sum(1.0 / q for q in points_quality)
        return center

    @staticmethod
    @contract
    def big_bang(center, sigma, number_of_points):
        """ Big Crunch procedure

            :param center: center of mass
            :type center: Vector

            :param sigma: scatter parameter
            :type sigma: number

            :param number_of_points: number of points to be generated
            :type number_of_points: int

            :returns: new points
            :rtype: list(Vector)
        """
        new_points = [center + Vector(values=np.random.normal(size=center.ndim) * sigma, keys=center.keys())
                      for _ in range(number_of_points)]
        return new_points

    def initialize(self, f, search_area, seed_state):
        initial_state = {}
        if seed_state is not None:
            raise NotImplementedError
        else:
            points = [tools.generate_vector_in_box(search_area) for _ in range(self._number_of_points)]
            initial_state["points"] = points
            initial_state["points_quality"], initial_state["best_value"] = BigBangBigCrunch.get_quality(points, np.inf, f)
            initial_state["iter_id"] = 1

        return initial_state

    def main_cycle(self, f, search_area, **kwargs):
        points = kwargs["points"]
        points_quality = kwargs["points_quality"]
        best_value = kwargs["best_value"]
        iter_id = kwargs["iter_id"]

        center = BigBangBigCrunch.big_crunch(points, points_quality)

        new_points = BigBangBigCrunch.big_bang(
            center,
            sigma=self._scatter_parameter / iter_id,
            number_of_points=self._number_of_points)
        new_points = [p.constrain(area=search_area) for p in new_points]

        new_points_quality, new_best_value = BigBangBigCrunch.get_quality(new_points, best_value, f)

        return {
            "points": new_points,
            "points_quality": new_points_quality,
            "best_value": new_best_value,
            "iter_id": iter_id + 1
        }

    def terminate(self, f, search_area, **kwargs):
        return BigBangBigCrunch.big_crunch(points=kwargs["points"], points_quality=kwargs["points_quality"])
