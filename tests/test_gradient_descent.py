"""Tests for Random Search."""


import numpy.linalg as la
import pytest
from osol.algorithms.gradient_descent import GradientDescent
from osol.smoke import generate_smoke_L2, generate_smoke_linear

EPS = 1e-3
TOL = 1e-2
NUM_ITER = [int(n) for n in (1e3, 1e5, 1e7)]

TEST_FUNCTIONS_LINEAR = (
    generate_smoke_linear(n_dim=1),
    generate_smoke_linear(n_dim=2),
    generate_smoke_linear(n_dim=3),
)

TEST_FUNCTIONS_L2 = (
    generate_smoke_L2(n_dim=1),
    generate_smoke_L2(n_dim=2),
    generate_smoke_L2(n_dim=3),
)


def test_algorithm_trace():
    """Test trace."""
    gd = GradientDescent(eps=EPS)
    f, f_grad = TEST_FUNCTIONS_L2[0]
    num_iter = NUM_ITER[0]
    gd.optimize(
        f,
        f_grad,
        f.search_area,
        num_iter,
        save_trace=True,
        verbose_attrs=["x", "y"],
    )
    trace = getattr(gd, "trace")
    assert len(trace) == num_iter + 2
    assert "x" in trace[0]
    assert "y" in trace[0]


@pytest.mark.parametrize("func", TEST_FUNCTIONS_LINEAR)
def test_algorithm_linear(func):
    """Smoke test: linear."""
    gd = GradientDescent(eps=EPS)
    success = False
    for num_iter in NUM_ITER:
        f = func[0]
        f_grad = func[1]
        sol = gd.optimize(f, f_grad, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success


@pytest.mark.parametrize("func", TEST_FUNCTIONS_L2)
def test_algorithm_L2(func):
    """Smoke test: L2."""
    gd = GradientDescent(eps=EPS)
    success = False
    for num_iter in NUM_ITER:
        f = func[0]
        f_grad = func[1]
        sol = gd.optimize(f, f_grad, f.search_area, num_iter)
        success = success or la.norm(sol - f.solution) < TOL
        if success:
            break
    assert success
