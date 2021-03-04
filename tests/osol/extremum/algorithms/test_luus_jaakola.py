import pytest

from osol.extremum.algorithms.luus_jaakola import LuusJaakola
from osol.extremum.tools.testing import smoke_check


@pytest.mark.parametrize("_", range(10))
def test_random_search(_):
    algorithm = LuusJaakola(
        init_radius=1.0,
        number_of_samples=5,
        reduction_coefficient=0.95,
        recover_coefficient=0.97,
        iteration_per_run=5,
    )
    assert smoke_check(algorithm, number_of_iterations=1000)
    try:
        state = algorithm.serialize()
        algorithm.deserialize(state)
        assert True
    except Exception:
        assert False
