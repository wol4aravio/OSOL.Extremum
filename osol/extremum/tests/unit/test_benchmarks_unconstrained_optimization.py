import numpy.testing as np_t
import pytest

from osol.extremum.optimization.benchmarks.unconstrained_optimization import *


@pytest.fixture(scope="session")
def n():
    return 5


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



