import numpy.testing as np_t
import pytest

from osol.extremum.optimization.benchmarks.unconstrained_optimization import *


@pytest.fixture(scope="session")
def n():
    return 5


def verify_benchmark(bf):
    np_t.assert_almost_equal(bf(bf.solution[0]), bf.solution[1])


def test_Ackley(n):
    verify_benchmark(Ackley(n))


def test_Alpine(n):
    verify_benchmark(Alpine(n))


def test_Bartels_Conn(n):
    verify_benchmark(Bartels_Conn())

