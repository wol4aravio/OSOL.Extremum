import pytest
import numpy as np

from osol.extremum.cybernetics.models.fmu_model import FMUModel


@pytest.fixture(scope="session")
def model():
    model = FMUModel(
        model="osol/extremum/tests/test_files/spacecraft_fmu/spacecraft.fmu",
        description="osol/extremum/tests/test_files/spacecraft_fmu/spacecraft.json",
        needs_compilation=True)
    yield model
    model._purge()


@pytest.fixture(scope="session")
def initial_state():
    return {
        "x1_0": 0.0,
        "x2_0": 0.0
    }


@pytest.fixture(scope="session")
def best_control():
    return {
        "a": -37.69911184307752,
        "b": 18.84955592153876
    }


@pytest.fixture(scope="session")
def steps():
    return [1e-3, 1e-5]


@pytest.fixture(scope="session")
def target_values():
    return np.pi, 0.0


@pytest.fixture(scope="session")
def eps():
    return 1e-3


def test_simulation(model, initial_state, best_control, steps, target_values, eps):
    errors = []
    x1_last_target, x2_last_target = target_values
    for step in steps:
        sim_result, _ = model.simulate(
            initial_state=initial_state,
            termination_time=1.0,
            dt=step,
            controllers={
                "u": {
                    "f": lambda t: best_control["a"] * t + best_control["b"],
                    "inputs": ["t"]
                }
            })

        x1_last = sim_result["x1"][-1]
        x2_last = sim_result["x2"][-1]

        errors.append(np.sqrt(np.square(x1_last_target - x1_last) + np.square(x2_last_target - x2_last)))

    for i, e in enumerate(errors[:-1]):
        assert e > errors[i + 1]

    assert errors[-1] < eps
