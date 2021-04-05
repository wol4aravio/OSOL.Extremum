# pylint: disable=protected-access

import numpy as np
import numpy.testing as npt
import pytest

from osol.extremum.algorithms.testing import FeldbaumTestFunctions


@pytest.mark.parametrize("_", range(10))
def test_1(_):
    f = FeldbaumTestFunctions(N=1, dim=2)
    npt.assert_almost_equal(f(f._c[0, :]), f._b)


@pytest.mark.parametrize("_", range(10))
def test_2(_):
    N = 10
    f = FeldbaumTestFunctions(N, dim=2)
    min_b = np.min(f._b)
    npt.assert_almost_equal(np.min([f(f._c[i, :]) for i in range(N)]), min_b)


def test_3():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5], [6]])
    c = np.array([[7, 8], [9, 10]])
    p = np.array([[0.5, 2], [2, 0.5]])
    f = FeldbaumTestFunctions(N=2, dim=2, random=False, a=a, b=b, c=c, p=p)
    npt.assert_almost_equal(f(np.array([7, 8])), 5.0)

    x = np.array([1, 2])

    part_11 = a[0, 0] * np.abs(x[0] - c[0, 0]) ** p[0, 0]
    part_12 = a[0, 1] * np.abs(x[1] - c[0, 1]) ** p[0, 1]
    part_1 = part_11 + part_12 + b[0, 0]

    part_21 = a[1, 0] * np.abs(x[0] - c[1, 0]) ** p[1, 0]
    part_22 = a[1, 1] * np.abs(x[1] - c[1, 1]) ** p[1, 1]
    part_2 = part_21 + part_22 + b[1, 0]

    npt.assert_almost_equal(f(x), np.min([part_1, part_2]))
