import pytest

from osol.extremum.algorithms.random_search import RandomSearch
from osol.extremum.tools.testing import smoke_check


@pytest.mark.parametrize("_", range(10))
def test_random_search(_):
    algorithm = RandomSearch(1e-1)
    assert smoke_check(algorithm, number_of_iterations=2500)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
