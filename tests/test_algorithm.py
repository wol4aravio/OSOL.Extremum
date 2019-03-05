from typing import Callable, List, Tuple
import time

import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal

from intervallum.box import Box, BoxVector
from intervallum.interval import Interval, IntervalNumber
from osol.extremum.algorithm import FunctionWithCounter, FunctionWithTimer

from osol.extremum.algorithms.constrained_random_search import ConstrainedRandomSearch as CRS
from osol.extremum.algorithms.interval_explosion_search import IntervalExplosionSearch as IES
from osol.extremum.algorithms.statistical_anti_gradient_random_search import StatisticalAntiGradientRandomSearch as SAG_RS


@pytest.fixture(scope="session")
def f() -> Callable[[BoxVector], IntervalNumber]:
    return lambda v: sum(np.power(v, 2))


@pytest.fixture(scope="session")
def area() -> List[Tuple[float, float]]:
    return [(-10.0, 10.0)] * 3


@pytest.fixture(scope="session")
def x_best() -> np.ndarray:
    return np.zeros(3)


@pytest.fixture(scope="session")
def test_f() -> Callable[[BoxVector], IntervalNumber]:
    return lambda v: v[0] + v[1] + v[2]


@pytest.fixture(scope="session")
def v() -> List[BoxVector]:
    return [np.array([1, 2, 3]), Box(Interval(1, 2), 3.0, 4.0)]


def test_counter(test_f: Callable[[BoxVector], IntervalNumber],
                 v: List[BoxVector]):
    f_ = FunctionWithCounter(test_f, max_number_of_calls=10)
    result = [f_(v_) for v_ in v * 5]
    assert result is not None
    with pytest.raises(TimeoutError):
        _ = f_(v[0])
    with pytest.raises(TimeoutError):
        _ = f_(v[1])


def test_timer(test_f: Callable[[BoxVector], IntervalNumber],
               v: List[BoxVector]):
    def sleep_sec(x: BoxVector) -> IntervalNumber:
        time.sleep(1.0)
        return test_f(x)
    f_ = FunctionWithTimer(sleep_sec, max_number_of_seconds=2.0)
    result = [f_(v_) for v_ in v]
    assert result is not None
    with pytest.raises(TimeoutError):
        _ = f_(v[0])
    with pytest.raises(TimeoutError):
        _ = f_(v[1])


def test_CRS(f: Callable[[BoxVector], IntervalNumber],
             area: List[Tuple[float, float]],
             x_best: np.ndarray):
    x = np.random.uniform(
        low=[x[0] for x in area],
        high=[x[1] for x in area],
        size=3)

    tool = CRS(max_shift=1e-1)

    tool.initialize(x=x)
    result_timer = tool.optimize_max_runtime(f, area, max_seconds=2.5)
    assert_array_almost_equal(result_timer, x_best, decimal=3)

    tool.initialize(x=x)
    result_timer = tool.optimize_max_calls(f, area, max_calls=2500)
    assert_array_almost_equal(result_timer, x_best, decimal=3)


def test_IES(f: Callable[[BoxVector], IntervalNumber],
             area: List[Tuple[float, float]],
             x_best: np.ndarray):
    points = np.random.uniform(
        low=[x[0] for x in area],
        high=[x[1] for x in area],
        size=(10, 3))

    bombs = []
    for i in range(points.shape[0] // 2):
        b = []
        for j in range(3):
            p1 = points[2 * i + 0, j]
            p2 = points[2 * i + 1, j]
            if p1 <= p2:
                b.append(Interval(p1, p2))
            else:
                b.append(Interval(p2, p1))
        bombs.append(Box(*b))

    tool = IES(max_radius=[0.1] * 3)

    tool.initialize(bombs=bombs, f=f)
    result_timer = tool.optimize_max_runtime(f, area, max_seconds=2.5)
    assert_array_almost_equal(result_timer, x_best, decimal=3)

    tool.initialize(bombs=bombs, f=f)
    result_timer = tool.optimize_max_calls(f, area, max_calls=2500)
    assert_array_almost_equal(result_timer, x_best, decimal=3)


def test_SAG_RS(f: Callable[[BoxVector], IntervalNumber],
                area: List[Tuple[float, float]],
                x_best: np.ndarray):
    x = np.random.uniform(
        low=[x[0] for x in area],
        high=[x[1] for x in area],
        size=3)

    tool = SAG_RS(radius=1e-1, number_of_samples=10)

    tool.initialize(x=x, f=f)
    result_timer = tool.optimize_max_runtime(f, area, max_seconds=2.5)
    assert_array_almost_equal(result_timer, x_best, decimal=3)

    tool.initialize(x=x, f=f)
    result_timer = tool.optimize_max_calls(f, area, max_calls=7500)
    assert_array_almost_equal(result_timer, x_best, decimal=3)
