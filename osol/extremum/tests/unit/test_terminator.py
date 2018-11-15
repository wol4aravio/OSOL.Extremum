import pytest
from datetime import datetime as dt
import math

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.optimization.basic.terminator import \
    DummyTerminator, MaxCallsTerminator, MaxTimeTerminator, TerminatorExceptions


@pytest.fixture(scope="session")
def v():
    return Vector.create(x=1, y=2, z=3)


@pytest.fixture(scope="session")
def f():
    return lambda x, y, z: x + y + z


@pytest.fixture(scope="session")
def f_dummy():
    return lambda v: v[0] + v['y'] + v[2]


@pytest.fixture(scope="session")
def eps():
    return 1e-2


@pytest.fixture
def dummy_terminator(f_dummy):
    return DummyTerminator(f_dummy, mode='dummy')


@pytest.fixture
def max_calls_terminator(f):
    return MaxCallsTerminator(f, mode='dict', max_calls=10)


@pytest.fixture
def max_time_terminator(f):
    return MaxTimeTerminator(f, mode='list', max_time="s:1.0")


def test_wrong_mode(f_dummy):
    with pytest.raises(TerminatorExceptions.UnsupportedModeException):
        _ = DummyTerminator(f_dummy, mode='magic')


def test_dummy(v, f_dummy, dummy_terminator):
    assert f_dummy(v) == dummy_terminator(v)


def test_max_calls(v, f, max_calls_terminator):
    results = []
    try:
        while True:
            results.append(max_calls_terminator(v))
    except TerminatorExceptions.StopWorkException:
        assert len(results) == max_calls_terminator._max_calls
        assert all([r == f(*v) for r in results])
    with pytest.raises(TerminatorExceptions.StopWorkException):
        _ = max_calls_terminator(v)


def test_max_time(v, f, max_time_terminator, eps):
    start_time = dt.now()
    results = []
    try:
        while True:
            results.append(max_time_terminator(v))
    except TerminatorExceptions.StopWorkException:
        duration = dt.now() - start_time
        assert math.fabs(duration.total_seconds() - max_time_terminator._max_duration.total_seconds()) < eps
        assert all([r == f(*v) for r in results])
    with pytest.raises(TerminatorExceptions.StopWorkException):
        _ = max_time_terminator(v)
