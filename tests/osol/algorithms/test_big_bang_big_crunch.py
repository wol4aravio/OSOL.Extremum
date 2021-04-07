import pytest

from osol.algorithms.big_bang_big_crunch import BigBangBigCrunch
from osol.tools.testing import feldbaum_check, smoke_check


@pytest.mark.parametrize("_", range(10))
def test_smoke(_):
    algorithm = BigBangBigCrunch(N=25, radius=2.5)
    assert smoke_check(algorithm, number_of_iterations=100)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False


@pytest.mark.parametrize("_", range(10))
def test_feldbaum(_):
    algorithm = BigBangBigCrunch(N=25, radius=2.5)
    assert feldbaum_check(algorithm, number_of_iterations=100)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
