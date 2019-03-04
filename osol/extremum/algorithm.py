import sys
from abc import ABC, abstractmethod
from typing import Callable, List, Tuple
from datetime import datetime as dt
from datetime import timedelta

import numpy as np

from intervallum.interval import IntervalNumber
from intervallum.box import BoxVector


def check_args(necessary_args: List[str], **kwargs):
    for arg in necessary_args:
        if arg not in kwargs:
            raise Exception(f"No necessary arguments: {arg}")
    return True


class Algorithm(ABC):

    @abstractmethod
    def initialize(self, **kwargs):
        ...

    @abstractmethod
    def optimize(
            self,
            f: Callable[[BoxVector], IntervalNumber],
            search_area: List[Tuple[float, float]],
            max_iterations: int) -> np.ndarray:
        ...

    @abstractmethod
    def terminate(self) -> np.ndarray:
        ...

    def optimize_max_calls(
            self, f: Callable[[BoxVector], IntervalNumber],
            search_area: List[Tuple[float, float]],
            max_calls: int) -> np.ndarray:
        try:
            return self.optimize(
                FunctionWithCounter(f, max_calls),
                search_area,
                max_iterations=sys.maxsize)
        except TimeoutError:
            return self.terminate()

    def optimize_max_runtime(
            self, f: Callable[[BoxVector], IntervalNumber],
            search_area: List[Tuple[float, float]],
            max_seconds: float) -> np.ndarray:
        try:
            return self.optimize(
                FunctionWithTimer(f, max_seconds),
                search_area,
                max_iterations=sys.maxsize)
        except TimeoutError:
            return self.terminate()


class FunctionWithCounter:
    def __init__(self,
                 f: Callable[[BoxVector], IntervalNumber],
                 max_number_of_calls: int):
        self._f = f
        self._number_of_calls = 0
        self._max_number_of_calls = max_number_of_calls

    def __call__(self, x: BoxVector) -> IntervalNumber:
        if self._number_of_calls >= self._max_number_of_calls:
            raise TimeoutError("Exceeded maximum number of allowed calls: " +
                               str(self._max_number_of_calls))
        self._number_of_calls += 1
        return self._f(x)


class FunctionWithTimer:
    def __init__(self,
                 f: Callable[[BoxVector], IntervalNumber],
                 max_number_of_seconds: float):
        self._f = f
        self._start = dt.utcnow()
        self.max_number_of_seconds = timedelta(seconds=max_number_of_seconds)

    def __call__(self, x: BoxVector) -> IntervalNumber:
        if dt.utcnow() - self._start >= self.max_number_of_seconds:
            raise TimeoutError("Exceeded allowed working time: " +
                               str(self.max_number_of_seconds))
        return self._f(x)
