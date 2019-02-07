from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

import numpy as np

from intervallum.interval import IntervalNumber
from intervallum.box import BoxVector


class Algorithm(ABC):

    @abstractmethod
    def optimize(
            self,
            f: Callable[[BoxVector], IntervalNumber],
            search_area: List[Tuple[float, float]],
            max_iterations: int) -> np.ndarray:
        ...


    def optimize_max_runtime(
            self,
            f: Callable[[BoxVector], IntervalNumber],
            search_area: List[Tuple[float, float]],
            max_time: int) -> np.ndarray:
        ...


class FunctionWithCounter:
    def __init__(self, f: Callable[[BoxVector], IntervalNumber], max_number_of_calls: int):
        self._f = f
        self._number_of_calls = 0
        self._max_number_of_calls = max_number_of_calls

    def __call__(self, x: BoxVector) -> IntervalNumber:
        if self._number_of_calls >= self._max_number_of_calls:
            raise Exception(f"Exceeded maximum number of allowed calls: {self._max_number_of_calls}")
        self._number_of_calls += 1
        return self._f(x)


