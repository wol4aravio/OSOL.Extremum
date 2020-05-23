"""Test smoke functions."""


import numpy as np
import numpy.testing as npt
from osol.smoke import generate_smoke_L2


def test_smoke_L2():
    """Test Smoke L2 function."""
    for n_dim in (1, 3, 5):
        f, f_grad = generate_smoke_L2(n_dim)
        npt.assert_almost_equal(f(f.solution), 0)
        npt.assert_almost_equal(f_grad(f.solution), np.zeros(shape=(n_dim,)))
        assert (f.search_area[:, 0] <= f.solution).all()
        assert (f.solution <= f.search_area[:, 1]).all()
