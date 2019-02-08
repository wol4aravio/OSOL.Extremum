from typing import Callable, List
import time

import pytest
import numpy as np

from intervallum.box import Box, BoxVector
from intervallum.interval import Interval, IntervalNumber
from osol.extremum.algorithm import FunctionWithCounter, FunctionWithTimer


@pytest.fixture(scope="session")
def f() -> Callable[[BoxVector], IntervalNumber]:
    return lambda v: v[0] + v[1] + v[2]


@pytest.fixture(scope="session")
def v() -> List[BoxVector]:
    return [np.array([1, 2, 3]), Box(Interval(1, 2), 3.0, 4.0)]


def test_counter(f: Callable[[BoxVector], IntervalNumber], v: List[BoxVector]):
    f_ = FunctionWithCounter(f, max_number_of_calls=10)
    result = [f_(v_) for v_ in v * 5]
    assert result is not None
    with pytest.raises(TimeoutError):
        _ = f_(v[0])
    with pytest.raises(TimeoutError):
        _ = f_(v[1])


def test_timer(f: Callable[[BoxVector], IntervalNumber], v: List[BoxVector]):
    def sleep_sec(x: BoxVector) -> IntervalNumber:
        time.sleep(1.0)
        return f(x)
    f_ = FunctionWithTimer(sleep_sec, max_number_of_seconds=2.0)
    result = [f_(v_) for v_ in v]
    assert result is not None
    with pytest.raises(TimeoutError):
        _ = f_(v[0])
    with pytest.raises(TimeoutError):
        _ = f_(v[1])
