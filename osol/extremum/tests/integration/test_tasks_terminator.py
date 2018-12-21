import pytest
from datetime import datetime as dt
import numpy as np

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.algorithms.terminator import \
    DummyTerminator, MaxCallsTerminator, MaxTimeTerminator, TerminatorExceptions

from osol.extremum.optimization.tasks.unconstrained_optimization import UnconstrainedOptimization


@pytest.fixture(scope="session")
def eps_error():
    return 1e-5


@pytest.fixture(scope="session")
def eps_time():
    return 1e-2


@pytest.fixture(scope="session")
def f_a():
    return lambda x, y, z: np.sin(x) + np.cos(y) - z


@pytest.fixture(scope="session")
def f_uo():
    return UnconstrainedOptimization(f="sin(x) + cos(y) - z", variables=["x", "y", "z"])


@pytest.fixture
def d_terminator(f_uo):
    return DummyTerminator(f_uo, mode='dict')


@pytest.fixture(scope="session")
def mc_terminator(f_uo):
    return MaxCallsTerminator(f=f_uo, mode="list", max_calls=10)


@pytest.fixture(scope="session")
def mt_terminator(f_uo):
    return MaxTimeTerminator(f=f_uo, mode="dict", max_time='s:1')


@pytest.fixture
def v():
    return Vector(np.random.uniform(-10.0, 10.0, size=3), ["x", "y", "z"])


def test_dummy(v, f_a, d_terminator, eps_error):
    assert np.abs(f_a(*v) - d_terminator(v)) < eps_error


def test_mc(v, f_a, mc_terminator, eps_error):
    results = []
    try:
        while True:
            results.append(mc_terminator(v))
    except TerminatorExceptions.StopWorkException:
        assert len(results) == mc_terminator._max_calls
        assert all([np.abs(r - f_a(*v)) < eps_error for r in results])
    with pytest.raises(TerminatorExceptions.StopWorkException):
        _ = mc_terminator(v)


def test_mt(v, f_a, mt_terminator, eps_time, eps_error):
    start_time = dt.now()
    results = []
    try:
        while True:
            results.append(mt_terminator(v))
    except TerminatorExceptions.StopWorkException:
        duration = dt.now() - start_time
        assert np.abs(duration.total_seconds() - mt_terminator._max_duration.total_seconds()) < eps_time
        assert all([np.abs(r - f_a(*v)) < eps_error for r in results])
    with pytest.raises(TerminatorExceptions.StopWorkException):
        _ = mt_terminator(v)
