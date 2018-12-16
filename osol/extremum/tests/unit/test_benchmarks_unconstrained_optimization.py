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


def test_Griewank(n):
    verify_benchmark(Griewank(n))


def test_GulfResearch():
    verify_benchmark(GulfResearch())


def test_Hansen():
    verify_benchmark(Hansen())


def test_HelicalValley():
    verify_benchmark(HelicalValley())


def test_Himmelblau():
    verify_benchmark(Himmelblau())


def test_Hosaki():
    verify_benchmark(Hosaki())


def test_JennrichSampson():
    verify_benchmark(JennrichSampson())


def test_Keane():
    verify_benchmark(Keane())


def test_Langermann():
    verify_benchmark(Langermann())


def test_Leon():
    verify_benchmark(Leon())


def test_Matyas():
    verify_benchmark(Matyas())


def test_McCormick():
    verify_benchmark(McCormick())


def test_MieleCantrell():
    verify_benchmark(MieleCantrell())


def test_MishraZeroSum(n):
    verify_benchmark(MishraZeroSum(n))


def test_Parsopoulos():
    verify_benchmark(Parsopoulos())


def test_PenHolder():
    verify_benchmark(PenHolder())


def test_Pathological(n):
    verify_benchmark(Pathological(n))


def test_Paviani():
    verify_benchmark(Paviani())


def test_Periodic():
    verify_benchmark(Periodic())


def test_Price():
    verify_benchmark(Price())


def test_Quadratic():
    verify_benchmark(Quadratic())


def test_Quintic(n):
    verify_benchmark(Quintic(n))


def test_Ripple():
    verify_benchmark(Ripple(5))
