import numpy as np
import pytest

from osol.extremum.optimization.basic.vector import Vector
from osol.extremum.optimization.basic.vector import VectorExceptions


@pytest.fixture(scope="session")
def v1_no_explicit_keys():
    return Vector.create(1, 2, _var_3=3)


@pytest.fixture(scope="session")
def v1_explicit_keys():
    return Vector(np.array([1, 2, 3]), ["x", "y", "z"])


@pytest.fixture(scope="session")
def v1_times_2_explicit_keys():
    return Vector(np.array([2, 4, 6]), ["x", "y", "z"])


@pytest.fixture(scope="session")
def v1_plus_2_explicit_keys():
    return Vector(np.array([3, 4, 5]), ["x", "y", "z"])


@pytest.fixture(scope="session")
def v2_explicit_keys():
    return Vector(np.array([1, 2]), ["x", "y"])


@pytest.fixture(scope="session")
def v3_explicit_keys():
    return Vector(np.array([1]), ["x"])


@pytest.fixture(scope="session")
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
    assert v1_explicit_keys.__str__() == "x -> 1.0, y -> 2.0, z -> 3.0"
    assert v3_explicit_keys.__repr__() == "x -> 1.0"


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

    with pytest.raises(KeyError):
        v1_copy[5] = -1
    with pytest.raises(KeyError):
        v1_copy["___"] = -1


def test_eq(v1_explicit_keys, v2_explicit_keys):
    assert v1_explicit_keys == v1_explicit_keys
    assert v1_explicit_keys != v2_explicit_keys
    assert v1_explicit_keys != v1_explicit_keys * 2


def test_multiplication(v1_explicit_keys, v1_times_2_explicit_keys):
    assert v1_explicit_keys * 2.0 == v1_times_2_explicit_keys
    assert (v1_explicit_keys * 2.0) * 3 == v1_times_2_explicit_keys * 3


def test_serialization(v1_explicit_keys):
    target_dict = {
        "Vector": {
            "x": 1.0,
            "y": 2.0,
            "z": 3.0
        }
    }
    serialized = v1_explicit_keys.to_dict()
    assert serialized == target_dict
    assert Vector.from_dict(serialized) == v1_explicit_keys


def test_addition(v1_explicit_keys, v2_explicit_keys, v1_plus_2_explicit_keys):
    assert v1_explicit_keys + v1_explicit_keys == v1_explicit_keys * 2
    assert v1_explicit_keys + 2 == v1_plus_2_explicit_keys
    with pytest.raises(VectorExceptions.DifferentKeysException):
        _ = v1_explicit_keys + v2_explicit_keys


def test_move(v1_no_explicit_keys):
    assert v1_no_explicit_keys.move((0, 1)) == Vector([2, 2, 3])
    assert v1_no_explicit_keys.move((0, 1), ("_var_1", 1), (0, 1)) == Vector([4, 2, 3])
    assert v1_no_explicit_keys.move(*v1_no_explicit_keys.to_tuples()) == v1_no_explicit_keys * 2
    assert v1_no_explicit_keys.move(**v1_no_explicit_keys) == v1_no_explicit_keys * 2


def test_constrain(v1_explicit_keys):
    assert v1_explicit_keys.constrain(("x", (-1, 2.0))) == v1_explicit_keys
    assert v1_explicit_keys.constrain(("x", (-1, 0.3))) == Vector([0.3, 2, 3], v1_explicit_keys.keys())
    assert v1_explicit_keys.constrain(("x", (-1, 0.3)), (0, (1.0, 2.0))) == Vector([1, 2, 3], v1_explicit_keys.keys())
