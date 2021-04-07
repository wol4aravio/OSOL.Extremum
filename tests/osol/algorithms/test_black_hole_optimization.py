import pytest

from osol.algorithms.black_hole_optimization import BlackHoleOptimization
from osol.tools.testing import feldbaum_check, smoke_check


@pytest.mark.parametrize("_", range(10))
def test_smoke(_):
    algorithm = BlackHoleOptimization(N=25)
    assert smoke_check(algorithm, number_of_iterations=100)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False


@pytest.mark.parametrize("_", range(10))
def test_feldbaum(_):
    algorithm = BlackHoleOptimization(N=25)
    assert feldbaum_check(algorithm, number_of_iterations=100)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
