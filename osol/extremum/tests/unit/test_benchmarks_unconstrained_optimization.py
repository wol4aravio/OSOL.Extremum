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


def test_Bartels_Conn(n):
    verify_benchmark(Bartels_Conn())


def test_Beale(n):
    verify_benchmark(Beale())


def test_Bird(n):
    verify_benchmark(Bird())


def test_Bohachevsky(n):
    verify_benchmark(Bohachevsky())


def test_Booth(n):
    verify_benchmark(Booth())

