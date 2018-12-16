import numpy.testing as np_t
import pytest

from osol.extremum.optimization.benchmarks.unconstrained_optimization import *


@pytest.fixture(scope="session")
def n():
    return 17


def verify_benchmark(bf):
    x_best, y_best = bf.solution
    np_t.assert_almost_equal(bf(x_best), y_best)
    assert x_best.belongs_to(bf.search_area)



def test_Ackley(n):
    verify_benchmark(Ackley(n))


def test_Alpine(n):
    verify_benchmark(Alpine(n))


def test_BartelssConn():
    verify_benchmark(BartelsConn())


def test_Beale():
    verify_benchmark(Beale())


def test_Bird():
    verify_benchmark(Bird())


def test_Bohachevsky():
    verify_benchmark(Bohachevsky())


def test_Booth():
    verify_benchmark(Booth())


def test_Brent():
    verify_benchmark(Brent())


def test_Brown(n):
    verify_benchmark(Brown(n))


def test_BoxBettsQuadraticSum(n):
    verify_benchmark(BoxBettsQuadraticSum())


def test_BraninRCOS(n):
    verify_benchmark(BraninRCOS())


def test_Bukin():
    verify_benchmark(Bukin())


def test_Chichinadze():
    verify_benchmark(Chichinadze())


def test_Colville():
    verify_benchmark(Colville())


def test_Corana():
    verify_benchmark(Corana())


def test_CosineMixture(n):
    verify_benchmark(CosineMixture(n))


def test_Csendes(n):
    verify_benchmark(Csendes(n))


def test_Cube():
    verify_benchmark(Cube())


def test_Damavandi():
    verify_benchmark(Damavandi())


def test_Deb(n):
    verify_benchmark(Deb(n))


def test_DeckkersAarts():
    verify_benchmark(DeckkersAarts())


def test_DixonAndPrice(n):
    verify_benchmark(DixonAndPrice(n))


def test_Dolan():
    verify_benchmark(Dolan())


def test_Easom():
    verify_benchmark(Easom())


def test_EggCrate():
    verify_benchmark(EggCrate())


def test_EggHolder():
    verify_benchmark(EggHolder())


def test_Exponential(n):
    verify_benchmark(Exponential(n))


def test_Goldstein():
    verify_benchmark(Goldstein())
