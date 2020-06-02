"""Tests for Random Search."""


import numpy.linalg as la
import pytest
from osol.algorithms.particle_swarm_optimization import (
    ParticleSwarmOptimization,
)
from osol.smoke import (
    generate_smoke_L1,
    generate_smoke_L2,
    generate_smoke_linear,
)

POP_SIZE = 25
VELOCITY_RATIO = 0.5
C0 = 0.9
C1 = 0.9
C2 = 0.9

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
    pso = ParticleSwarmOptimization(
        pop_size=POP_SIZE, velocity_ratio=VELOCITY_RATIO, c0=C0, c1=C1, c2=C2
    )
    f = TEST_FUNCTIONS_L2[0]
    num_iter = NUM_ITER[0]
    pso.optimize(
        f,
        f.search_area,
        num_iter,
        save_trace=True,
        verbose_attrs=["global_best", "global_best_value"],
    )
    trace = getattr(pso, "trace")
    assert len(trace) == num_iter + 2
    assert "global_best" in trace[0]
    assert "global_best_value" in trace[0]


@pytest.mark.parametrize("f", TEST_FUNCTIONS_LINEAR)
def test_algorithm_linear(f):
    """Smoke test: linear."""
    pso = ParticleSwarmOptimization(
        pop_size=POP_SIZE, velocity_ratio=VELOCITY_RATIO, c0=C0, c1=C1, c2=C2
    )
    success = False
    for num_iter in NUM_ITER:
        sol = pso.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("f", TEST_FUNCTIONS_L1)
def test_algorithm_L1(f):
    """Smoke test: L1."""
    pso = ParticleSwarmOptimization(
        pop_size=POP_SIZE, velocity_ratio=VELOCITY_RATIO, c0=C0, c1=C1, c2=C2
    )
    success = False
    for num_iter in NUM_ITER:
        sol = pso.optimize(f, f.search_area, num_iter, save_trace=True)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("f", TEST_FUNCTIONS_L2)
def test_algorithm_L2(f):
    """Smoke test: L2."""
    pso = ParticleSwarmOptimization(
        pop_size=POP_SIZE, velocity_ratio=VELOCITY_RATIO, c0=C0, c1=C1, c2=C2
    )
    success = False
    for num_iter in NUM_ITER:
        sol = pso.optimize(f, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success
