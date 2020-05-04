"""Test benchmark functions."""


import numpy.testing as npt
from osol.benchmarks import Ackley, Alpine

DIM = 5


def test_ackley():
    """Test Ackley function."""
    f = Ackley(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_alpine():
    """Test Alpine function."""
    f = Alpine(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
