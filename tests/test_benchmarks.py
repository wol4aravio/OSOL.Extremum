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
    Chichinadze,
    Colville,
    Corana,
    CosineMixture,
    Csendes,
    Cube,
    Damavandi,
    Deb,
    DeckkersAarts,
    DixonAndPrice,
    Dolan,
    Easom,
    EggCrate,
    EggHolder,
    Exponential,
    Goldstein,
    Griewank,
)

DIM = 5


def test_ackley():
    """Test Ackley function."""
    f = Ackley(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_alpine():
    """Test Alpine function."""
    f = Alpine(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_bartels_conn():
    """Test BartelsConn function."""
    f = BartelsConn()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_beale():
    """Test Beale function."""
    f = Beale()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_bird():
    """Test Bird function."""
    f = Bird()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_bohachevsky():
    """Test Bohachevsky function."""
    f = Bohachevsky()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_booth():
    """Test Booth function."""
    f = Booth()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_box_betts_quadratic_sum():
    """Test BoxBettsQuadraticSum function."""
    f = BoxBettsQuadraticSum()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_branin_rcos():
    """Test BraninRCOS function."""
    f = BraninRCOS()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_brent():
    """Test Brent function."""
    f = Brent()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_brown():
    """Test Brown function."""
    f = Brown(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_bukin():
    """Test Bukin function."""
    f = Bukin()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_camel_three_humps():
    """Test CamelThreeHumps function."""
    f = CamelThreeHumps()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_chichinadze():
    """Test Chichinadze function."""
    f = Chichinadze()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_colville():
    """Test Colville function."""
    f = Colville()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_corana():
    """Test Corana function."""
    f = Corana()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_cosine_mixture():
    """Test CosineMixture function."""
    f = CosineMixture(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_csendes():
    """Test Csendes function."""
    f = Csendes(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_cube():
    """Test Cube function."""
    f = Cube()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_damavandi():
    """Test Damavandi function."""
    f = Damavandi()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_deb():
    """Test Deb function."""
    f = Deb(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_deckkers_aarts():
    """Test DeckkersAarts function."""
    f = DeckkersAarts()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_dixon_and_price():
    """Test DixonAndPrice function."""
    f = DixonAndPrice(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_dolan():
    """Test Dolan function."""
    f = Dolan()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_easom():
    """Test Easom function."""
    f = Easom()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_eggCrate():
    """Test EggCrate function."""
    f = EggCrate()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_eggHolder():
    """Test EggHolder function."""
    f = EggHolder()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_exponential():
    """Test Exponential function."""
    f = Exponential(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_goldstein():
    """Test Goldstein function."""
    f = Goldstein()
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()


def test_griewank():
    """Test Griewank function."""
    f = Griewank(DIM)
    npt.assert_almost_equal(f(f.solution_x), f.solution_y)
    assert (f.search_area[:, 0] <= f.solution_x).all()
    assert (f.solution_x <= f.search_area[:, 1]).all()
