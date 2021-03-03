import numpy as np
import pytest

from osol.extremum.tools.vectors import generate_vector_in_sphere


@pytest.mark.parametrize("_", range(100))
def test_generate_vector_in_sphere(_):
    initial = np.array([0, 0, 0])
    radius = 2.5
    generated = generate_vector_in_sphere(initial, radius)
    assert np.linalg.norm(generated - initial) <= radius
