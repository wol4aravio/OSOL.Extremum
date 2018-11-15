import pytest
import numpy as np

from osol.extremum.optimization.tasks.unconstrained_optimization import UnconstrainedOptimization


@pytest.fixture(scope="session")
def eps():
    return 1e-7


@pytest.fixture(scope="session")
def f_a():
    return lambda x, y, z: np.sin(x) + np.cos(y) - z


@pytest.fixture(scope="session")
def f_uo():
    return UnconstrainedOptimization(f='sin(x) + cos(y) - z', variables=['x', 'y', 'z'])


def test(eps, f_a, f_uo):
    points = np.random.uniform(-10.0, 10.0, size=(17, 3))
    results_a = np.array([f_a(*r) for r in points])
    results_uo = np.array([f_uo(*r) for r in points])
    assert np.mean(np.abs(results_a - results_uo)) < eps
