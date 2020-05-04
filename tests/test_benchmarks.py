"""Test benchmark functions."""


import numpy.testing as npt
from osol.benchmarks import Ackley

DIM = 5


def test_ackley():
    """Test Ackley function."""
    f = Ackley(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
