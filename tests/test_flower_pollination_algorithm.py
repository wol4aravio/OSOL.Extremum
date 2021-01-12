"""Set of tests for parser tool."""


import numpy as np
from numpy.testing import assert_almost_equal

from osol.extremum.algorithms.flower_pollination_algorithm import FPA
from osol.extremum.tools.parser import OptTask


def test_fpa_smoke_1():
    """Test FPA for smoke_1 function."""
    fpa = FPA(N=10, p=0.2, gamma=0.1, lambda_=1.0)
    f = OptTask("osol/extremum/functions/smoke_1.opt")
    sol = np.array([0, 0])
    s = np.array([[-10, 10], [-10, 10]])
    N = 100
    assert_almost_equal(fpa.optimize(f, s, N), sol, decimal=3)
    state = fpa.serialize()
    fpa.deserialize(state)
    assert_almost_equal(fpa.terminate(f, s), sol, decimal=3)
