"""Tests for Random Search."""


import numpy.linalg as la
import pytest
from osol.algorithms.explosion_search import ExplosionSearch
from osol.smoke import (
    generate_smoke_L1,
    generate_smoke_L2,
    generate_smoke_linear,
)

B_MAX = 6
POWER_MAX = 1.0

TOL = 1e-1
NUM_ITER = [int(n) for n in (1e3, 1e4, 1e5)]

TEST_FUNCTIONS_LINEAR = (
    generate_smoke_linear(n_dim=1)[0],
    generate_smoke_linear(n_dim=2)[0],
    generate_smoke_linear(n_dim=3)[0],
)

TEST_FUNCTIONS_L1 = (
    generate_smoke_L1(n_dim=1),
    generate_smoke_L1(n_dim=2),
    generate_smoke_L1(n_dim=3),
)

TEST_FUNCTIONS_L2 = (
    generate_smoke_L2(n_dim=1)[0],
    generate_smoke_L2(n_dim=2)[0],
    generate_smoke_L2(n_dim=3)[0],
)


def test_algorithm_trace():
    """Test trace."""
    es = ExplosionSearch(b_max=B_MAX, power_max=POWER_MAX)
    f = TEST_FUNCTIONS_L2[0]
    num_iter = NUM_ITER[0]
    es.optimize(
        f, f.search_area, num_iter, save_trace=True, verbose_attrs=["bombs"]
    )
    trace = getattr(es, "trace")
    assert len(trace) == num_iter + 2
    assert "bombs" in trace[0]


@pytest.mark.parametrize("f", TEST_FUNCTIONS_LINEAR)
def test_algorithm_linear(f):
    """Smoke test: linear."""
    es = ExplosionSearch(b_max=B_MAX, power_max=POWER_MAX)
    success = False
    for num_iter in NUM_ITER:
        sol = es.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("f", TEST_FUNCTIONS_L1)
def test_algorithm_L1(f):
    """Smoke test: L1."""
    es = ExplosionSearch(b_max=B_MAX, power_max=POWER_MAX)
    success = False
    for num_iter in NUM_ITER:
        sol = es.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("f", TEST_FUNCTIONS_L2)
def test_algorithm_L2(f):
    """Smoke test: L2."""
    es = ExplosionSearch(b_max=B_MAX, power_max=POWER_MAX)
    success = False
    for num_iter in NUM_ITER:
        sol = es.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success
