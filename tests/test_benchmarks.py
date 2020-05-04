"""Test benchmark functions."""


import numpy.testing as npt
from osol.benchmarks import (
    Ackley,
    Alpine,
    BartelsConn,
    Beale,
    Bird,
    Bohachevsky,
    Booth,
    BoxBettsQuadraticSum,
    BraninRCOS,
    Brent,
    Brown,
    Bukin,
    CamelThreeHumps,
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


def test_booth():
    """Test Booth function."""
    f = Booth()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_box_betts_quadratic_sum():
    """Test BoxBettsQuadraticSum function."""
    f = BoxBettsQuadraticSum()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_branin_rcos():
    """Test BraninRCOS function."""
    f = BraninRCOS()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_brent():
    """Test Brent function."""
    f = Brent()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_brown():
    """Test Brown function."""
    f = Brown(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_bukin():
    """Test Bukin function."""
    f = Bukin()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)


def test_camel_three_humps():
    """Test CamelThreeHumps function."""
    f = CamelThreeHumps()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
