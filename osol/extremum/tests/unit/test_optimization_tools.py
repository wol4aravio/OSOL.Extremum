import pytest

from osol.extremum.optimization.algorithms.tools import *


@pytest.fixture(scope="session")
def number_of_vectors():
    return 10


@pytest.fixture(scope="session")
def area():
    return {
        "x": (-1.0, 1.0),
        "y": (-2.0, 2.0),
        "z": (-3.0, 3.0)
    }


def test_generate_vector(number_of_vectors, area):
    for _ in range(number_of_vectors):
        v = generate_vector(area)
        assert v == v.constrain(area=area)
