from typing import Callable, List, Tuple

import numpy as np

from osol.extremum.algorithm import Algorithm, check_args
from intervallum.box import BoxVector
from intervallum.box_functions import constrain
from intervallum.interval import IntervalNumber


class StatisticalAntiGradientRandomSearch(Algorithm):

    def __init__(self, radius, number_of_samples):
        self.radius = radius
        self.number_of_samples = number_of_samples

    def initialize(self, **kwargs):
        if check_args(["x", "f"], **kwargs):
            self.x = kwargs["x"]
            self.f_x = kwargs["f"](self.x)

    def terminate(self):
        return self.x

    def optimize(self, f: Callable[[BoxVector], IntervalNumber],
                 search_area: List[Tuple[float, float]],
                 max_iterations: int):
        iter_id = 0
        while iter_id < max_iterations:
            new_points = [
                np.random.uniform(self.x - self.radius, self.x + self.radius)
                for _ in range(self.number_of_samples)]
            new_values = [f(p) for p in new_points]

            anti_gradient = np.zeros(shape=len(search_area))
            for point, f_point in zip(new_points, new_values):
                anti_gradient -= (point - self.x) * (f_point - self.f_x)
            anti_grad_length = np.linalg.norm(anti_gradient)
            if anti_grad_length > 0.0:
                anti_gradient *= 1.0 / anti_grad_length

            x_new = constrain(
                self.x + anti_gradient * np.random.uniform(0.0, self.radius),
                search_area)
            f_x_new = f(x_new)

            if f_x_new < self.f_x:
                self.x = x_new
                self.f_x = f_x_new

        return self.terminate()
