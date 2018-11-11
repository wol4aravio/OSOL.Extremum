import numpy as np
import pytest

from osol.extremum.optimization.basic.vector import Vector


@pytest.fixture(scope="session", autouse=True)
def v1_no_explicit_keys():
    return Vector([1, 2, 3])


@pytest.fixture(scope="session", autouse=True)
def v1_explicit_keys():
    return Vector(np.array([1, 2, 3]), ["x", "y", "z"])


@pytest.fixture(scope="session", autouse=True)
def v2_explicit_keys():
    return Vector(np.array([1, 2]), ["x", "y"])


@pytest.fixture(scope="session", autouse=True)
def v3_explicit_keys():
    return Vector(np.array([1]), ["x"])


@pytest.fixture(scope="session", autouse=True)
def eps():
    return 1e-7


def small_error(a, b, eps):
    return np.abs(a - b) < eps


def test_indexer(v1_no_explicit_keys):
    assert v1_no_explicit_keys[0] == 1
    assert v1_no_explicit_keys["_var_1"] == 1
    assert v1_no_explicit_keys[1] == v1_no_explicit_keys["_var_2"]
    with pytest.raises(KeyError):
        _ = v1_no_explicit_keys[5]
    with pytest.raises(KeyError):
        _ = v1_no_explicit_keys["_var_10"]


def test_str(v1_explicit_keys, v3_explicit_keys):
    assert v1_explicit_keys.__str__() == "x -> 1, y -> 2, z -> 3"
    assert v3_explicit_keys.__str__() == "x -> 1"


def test_iteration(v1_no_explicit_keys):
    for i, v in zip(range(len(v1_no_explicit_keys)), v1_no_explicit_keys):
        assert v == v1_no_explicit_keys[i]


def test_vector_to_list_or_dict(v1_explicit_keys, eps):
    def f(x, y, z):
        return x + y + z

    assert small_error(f(*v1_explicit_keys), 6.0, eps)
    assert small_error(f(**v1_explicit_keys), 6.0, eps)


def test_len(v1_explicit_keys, v2_explicit_keys, v3_explicit_keys):
    assert len(v1_explicit_keys) == 3
    assert len(v2_explicit_keys) == 2
    assert len(v3_explicit_keys) == 1


def test_set_element(v1_explicit_keys):
    v1_copy = v1_explicit_keys.copy()

    assert v1_copy[0] == 1
    v1_copy[0] = 2
    v1_copy["y"] = 3
    assert v1_copy[0] == 2
    assert v1_copy["y"] == 3
    assert v1_explicit_keys[0] == 1
    v1_explicit_keys[0] = 2
    assert v1_explicit_keys[0] == 2

    with pytest.raises(KeyError):
        v1_copy[5] = -1
    with pytest.raises(KeyError):
        v1_copy["___"] = -1
