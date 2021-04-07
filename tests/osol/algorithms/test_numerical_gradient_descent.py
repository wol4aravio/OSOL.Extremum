import pytest

from osol.algorithms.numerical_gradient_descent import NumericalGradientDescent
from osol.tools.testing import smoke_check


@pytest.mark.parametrize("_", range(10))
def test_random_search_smoke(_):
    algorithm = NumericalGradientDescent(1.0)
    assert smoke_check(algorithm, number_of_iterations=500)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
