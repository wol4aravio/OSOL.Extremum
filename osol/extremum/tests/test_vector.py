import pytest

from osol.extremum.optimization.basic.vector import Vector


@pytest.fixture(scope="session", autouse=True)
def v1_no_explicit_keys():
    return Vector([1, 2, 3])


def test_indexer(v1_no_explicit_keys):
    assert v1_no_explicit_keys[0] == 1
    assert v1_no_explicit_keys["_var_1"] == 1
    assert v1_no_explicit_keys[1] == v1_no_explicit_keys["_var_2"]

