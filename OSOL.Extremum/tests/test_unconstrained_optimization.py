from Tools.Encoders import CustomEncoder
from Optimization.Tasks.UnconstrainedOptimization import UnconstrainedOptimization
from Numerical_Objects.Interval import Interval as I
from Numerical_Objects.Vector import Vector as V

from math import fabs
import json


task = {
    'f': '1 * x ** 2 + 2 * y ** 2 + 3 * z ** 2',
    'variables': ['x', 'y', 'z']
}

tol = 1e-7


def almost_equal_real(v1, v2):
    return fabs(v1 - v2) < tol


def almost_equal_interval(i1, i2):
    return fabs(i1.left - i2.left) + fabs(i1.right - i2.right) < 2 * tol


def test_from_json():
    f = UnconstrainedOptimization.from_dict(task)
    assert f._f == UnconstrainedOptimization.from_json(json.dumps(f, cls=CustomEncoder))._f
    assert f._variables == UnconstrainedOptimization.from_json(json.dumps(f, cls=CustomEncoder))._variables


def test_real_calculation():
    f = UnconstrainedOptimization.from_dict(task)
    assert almost_equal_real(f({'x': 1, 'y': 2, 'z': 3}), 36.0)
    assert almost_equal_real(f({'x': -1, 'y': -2, 'z': -3}), 36.0)
    assert almost_equal_real(f({'x': 2, 'y': 2, 'z': 2}), 24.0)


def test_interval_calculation():
    f = UnconstrainedOptimization.from_dict(task)
    assert almost_equal_interval(f({'x': I(1, 2), 'y': I(2, 3), 'z': I(3, 4)}), I(36.0, 70.0))


def test_mixed_calculation():
    f = UnconstrainedOptimization.from_dict(task)
    assert almost_equal_interval(f(V({'x': I(1, 2), 'y': 2, 'z': 3})), I(36.0, 39.0))
