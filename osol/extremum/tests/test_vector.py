import pytest

from osol.extremum.optimization.basic.vector import Vector


@pytest.fixture(scope="session", autouse=True)
def v1():
    return Vector([1, 2, 3])


