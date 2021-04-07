# pylint: disable=protected-access

import numpy as np
import numpy.testing as npt
import pytest

from osol.tools.testing import FeldbaumTestFunctions


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
