from typing import Callable, List, Tuple

import numpy as np

from intervallum.box import BoxVector
from intervallum.box_functions import constrain
from intervallum.interval import IntervalNumber
from osol.extremum.algorithm import Algorithm


class ConstrainedRandomSearch(Algorithm):

    def __init__(self, max_shift: float):
        self.max_shift = max_shift

    def initialize(self, **kwargs):
        necessary_args = ["x"]
        for arg in necessary_args:
            if arg not in kwargs:
                raise Exception(f"No necessary arguments: {arg}")
        self.x = kwargs["x"]

    def terminate(self):
        return self.x

    def optimize(self, f: Callable[[BoxVector], IntervalNumber],
                 search_area: List[Tuple[float, float]],
                 max_iterations: int) -> np.ndarray:
        iter_id = 0
        dim = len(self.x)
        self.f = f(self.x)
        while iter_id < max_iterations:
            shift = np.random.uniform(low=-1.0, high=1.0, size=dim)
            shift /= np.linalg.norm(shift)
            shift *= np.random.uniform(low=0, high=self.max_shift)
            new_x = constrain(self.x + shift, search_area)
            new_f = f(new_x)
            if new_f <= self.f:
                self.x = new_x
                self.f = new_f
            iter_id += 1
        return self.terminate()
