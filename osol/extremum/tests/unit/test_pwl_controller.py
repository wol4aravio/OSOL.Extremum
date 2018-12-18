import pytest

import numpy as np

from osol.extremum.cybernetics.controllers_and_tools.pwl_controller import PWLController
from osol.extremum.cybernetics.controllers_and_tools.exceptions import ControlGenerationException


@pytest.fixture(scope="session")
def controller():
    return PWLController(time_grid=[0, 1, 3], values=[0, -1, 3])


@pytest.fixture(scope="session")
def eps():
    return 1e-7


def test_controller(controller, eps):
    eq = lambda a, b: np.abs(a - b) < eps
    assert eq(controller(0), 0.0)
    assert eq(controller(1), -1.0)
    assert eq(controller(3), 3.0)
    assert eq(controller(1.5), 0.0)
    assert eq(controller(2), 1.0)
    assert eq(controller(2.5), 2.0)
    with pytest.raises(ControlGenerationException):
        _ = controller(-1)
    with pytest.raises(ControlGenerationException):
        _ = controller(1e3)
