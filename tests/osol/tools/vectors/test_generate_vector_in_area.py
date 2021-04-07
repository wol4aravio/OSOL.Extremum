import numpy as np
import pytest

from osol.tools.vectors import generate_vector_in_area


@pytest.mark.parametrize("_", range(100))
def test_generate_vector_in_area(_):
    search_area = np.array([[-10, 10], [-10, 10]])
    vector = generate_vector_in_area(search_area)
    assert ((search_area[:, 0] <= vector) & (vector <= search_area[:, 1])).all()
