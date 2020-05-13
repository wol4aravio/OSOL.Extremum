"""Tests for Random Search."""


import numpy.linalg as la
import pytest
from osol.algorithms.random_search import RandomSearch
from osol.smoke import generate_smoke_L2

EPS = 1e-3
TOL = 1e-2
NUM_ITER = [int(n) for n in (1e3, 1e5, 1e7)]

TEST_FUNCTIONS = (
    generate_smoke_L2(n_dim=1),
    generate_smoke_L2(n_dim=2),
    generate_smoke_L2(n_dim=3),
)


@pytest.mark.parametrize("f", TEST_FUNCTIONS)
def test_algorithm(f):
    """Smoke test."""
    rs = RandomSearch(eps=EPS)
    success = False
    for num_iter in NUM_ITER:
        sol = rs.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success
