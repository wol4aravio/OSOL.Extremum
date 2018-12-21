import pytest
import numpy as np
import numpy.testing as np_t

from osol.extremum.algorithms.tools import belongs_to, length, constrain


@pytest.fixture(scope="session")
def v():
    return np.array([1, 2, 3])


def test_max_time(v):
    np_t.assert_almost_equal(length(v) ** 2, 14.0)


def test_belongs_to(v):
    assert belongs_to(v, [(-1, 1), (-2, 2), (-3, 3)])
    assert belongs_to(v, [(-1, 10), (-2, 20), (-3, 30)])
    assert not belongs_to(v, [(-1, 0.1), (-2, 0.2), (-3, 0.3)])


def test_constrain(v):
    np_t.assert_almost_equal(v, constrain(v, [(-1, 1), (-2, 2), (-3, 3)]))
    np_t.assert_almost_equal(constrain(v, [(0, 1), (3, 4), (0, 1)]), np.array([1, 3, 1]))
