import pytest

from osol.extremum.algorithms.statistical_anti_gradient_random_search import (
    StatisticalAntiGradientRandomSearch,
)
from osol.extremum.tools.testing import smoke_check


@pytest.mark.parametrize("_", range(10))
def test_random_search_smoke(_):
    algorithm = StatisticalAntiGradientRandomSearch(1e-1, 5)
    assert smoke_check(algorithm, number_of_iterations=500)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
