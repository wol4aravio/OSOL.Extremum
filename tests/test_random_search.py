"""Tests for Random Search."""


import numpy.linalg as la
import pytest
from osol.algorithms.random_search import RandomSearch
from osol.smoke import (
    generate_smoke_L1,
    generate_smoke_L2,
    generate_smoke_linear,
)

EPS = 1e-3
TOL = 1e-2
NUM_ITER = [int(n) for n in (1e3, 1e5, 1e7)]

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
    rs = RandomSearch(eps=EPS)
    f = TEST_FUNCTIONS_L2[0]
    num_iter = NUM_ITER[0]
    rs.optimize(
        f, f.search_area, num_iter, save_trace=True, verbose_attrs=["x", "y"]
    )
    assert len(rs.trace) == num_iter + 2
    assert "x" in rs.trace[0]
    assert "y" in rs.trace[0]


@pytest.mark.parametrize("f", TEST_FUNCTIONS_LINEAR)
def test_algorithm_linear(f):
    """Smoke test: linear."""
    rs = RandomSearch(eps=EPS)
    success = False
    for num_iter in NUM_ITER:
        sol = rs.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("f", TEST_FUNCTIONS_L1)
def test_algorithm_L1(f):
    """Smoke test: L1."""
    rs = RandomSearch(eps=EPS)
    success = False
    for num_iter in NUM_ITER:
        sol = rs.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("f", TEST_FUNCTIONS_L2)
def test_algorithm_L2(f):
    """Smoke test: L2."""
    rs = RandomSearch(eps=EPS)
    success = False
    for num_iter in NUM_ITER:
        sol = rs.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success
