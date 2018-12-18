import pytest
import numpy.testing as np_t

from osol.extremum.cybernetics.controllers_and_tools.saturation_limiter import SaturationLimiter


@pytest.fixture(scope="session")
def limiter_1():
    return SaturationLimiter(min_value=-1.0)


@pytest.fixture(scope="session")
def limiter_2():
    return SaturationLimiter(max_value=1.0)


@pytest.fixture(scope="session")
def limiter_3():
    return SaturationLimiter(min_value=-1.0, max_value=1.0)


def test_limiter_1(limiter_1):
    np_t.assert_almost_equal(limiter_1.check(-2.0), -1.0)
    np_t.assert_almost_equal(limiter_1.check(0.0), 0.0)
    np_t.assert_almost_equal(limiter_1.check(2.0), 2.0)


def test_limiter_2(limiter_2):
    np_t.assert_almost_equal(limiter_2.check(-2.0), -2.0)
    np_t.assert_almost_equal(limiter_2.check(0.0), 0.0)
    np_t.assert_almost_equal(limiter_2.check(2.0), 1.0)


def test_limiter_3(limiter_3):
    np_t.assert_almost_equal(limiter_3.check(-2.0), -1.0)
    np_t.assert_almost_equal(limiter_3.check(0.0), 0.0)
    np_t.assert_almost_equal(limiter_3.check(2.0), 1.0)
