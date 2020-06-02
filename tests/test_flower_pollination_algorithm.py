"""Tests for Random Search."""


import numpy.linalg as la
import pytest
from osol.algorithms.flower_pollination_algorithm import (
    FlowerPollinationAlgorithm,
)
from osol.smoke import (
    generate_smoke_L1,
    generate_smoke_L2,
    generate_smoke_linear,
)

POP_SIZE = 25
SWITCH_PROB = 0.9
GAMMA = 0.25
LAMBDA_VALUE = 1.25

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
    rs = FlowerPollinationAlgorithm(
        pop_size=POP_SIZE,
        switch_prob=SWITCH_PROB,
        gamma=GAMMA,
        lambda_value=LAMBDA_VALUE,
    )
    f = TEST_FUNCTIONS_L2[0]
    num_iter = NUM_ITER[0]
    rs.optimize(
        f,
        f.search_area,
        num_iter,
        save_trace=True,
        verbose_attrs=["best_x", "best_y"],
    )
    trace = getattr(rs, "trace")
    assert len(trace) == num_iter + 2
    assert "best_x" in trace[0]
    assert "best_y" in trace[0]


@pytest.mark.parametrize("f", TEST_FUNCTIONS_LINEAR)
def test_algorithm_linear(f):
    """Smoke test: linear."""
    rs = FlowerPollinationAlgorithm(
        pop_size=POP_SIZE,
        switch_prob=SWITCH_PROB,
        gamma=GAMMA,
        lambda_value=LAMBDA_VALUE,
    )
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
    rs = FlowerPollinationAlgorithm(
        pop_size=POP_SIZE,
        switch_prob=SWITCH_PROB,
        gamma=GAMMA,
        lambda_value=LAMBDA_VALUE,
    )
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
    rs = FlowerPollinationAlgorithm(
        pop_size=POP_SIZE,
        switch_prob=SWITCH_PROB,
        gamma=GAMMA,
        lambda_value=LAMBDA_VALUE,
    )
    success = False
    for num_iter in NUM_ITER:
        sol = rs.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success
