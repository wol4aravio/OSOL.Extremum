import pytest

from osol.extremum.algorithms.random_search import RandomSearch
from osol.extremum.tools.testing import feldbaum_check, smoke_check


@pytest.mark.parametrize("_", range(10))
def test_random_search_smoke(_):
    algorithm = RandomSearch(1.0)
    assert smoke_check(algorithm, number_of_iterations=1000)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False


@pytest.mark.parametrize("_", range(10))
def test_random_search_Feldbaum(_):
    algorithm = RandomSearch(1.0)
    assert feldbaum_check(algorithm, number_of_iterations=1000, eps=1e-1)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
