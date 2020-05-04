"""Test benchmark functions."""


import numpy.testing as npt
from osol.benchmarks import (
    Ackley,
    Alpine,
    BartelsConn,
    Beale,
    Bird,
    Bohachevsky,
)

DIM = 5


def test_ackley():
    """Test Ackley function."""
    f = Ackley(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_alpine():
    """Test Alpine function."""
    f = Alpine(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_bartels_conn():
    """Test BartelsConn function."""
    f = BartelsConn()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_beale():
    """Test Beale function."""
    f = Beale()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_bird():
    """Test Bird function."""
    f = Bird()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_bohachevsky():
    """Test Bohachevsky function."""
    f = Bohachevsky()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
