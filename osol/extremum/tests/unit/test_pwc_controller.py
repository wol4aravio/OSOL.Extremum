import pytest
import numpy as np

from osol.extremum.cybernetics.controllers.pwc_controller import PWCController
from osol.extremum.cybernetics.controllers.exceptions import ControlGenerationException


@pytest.fixture(scope="session")
def controller():
    return PWCController(time_grid=np.arange(0.0, 1.1, 0.1), values=list(range(0, 11)))


def test_controller(controller):
    assert controller(0) == 0
    assert controller(0.01) == 0
    with pytest.raises(ControlGenerationException):
        _ = controller(-1)
    assert controller(1e9) == 10
