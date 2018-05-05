import os
from math import fabs

from OSOL_Extremum.computational_core.computational_core import *

file_writer = open('temp.json', 'w')
file_writer.writelines("""
{
	"task_type": "unconstrained_optimization",
	"f": "1 * x ** 2 + 2 * y ** 2 + 3 * z ** 2",
	"vars": ["x", "y", "z"],
	"differentiable": true,
	"area": [
		{ "name": "x", "min": -10.0, "max": 10.0 },
		{ "name": "y", "min": -10.0, "max": 10.0 },
		{ "name": "z", "min": -10.0, "max": 10.0 }
	],
	"solution": [
		{ "name": "x", "value": 0.0 },
		{ "name": "y", "value": 0.0 },
		{ "name": "z", "value": 0.0 }
	]
}""")
file_writer.close()

core = ComputationalCore.from_json('temp.json')

tol = 1e-7


def almost_equal(v1, v2):
    return fabs(v1 - v2) < tol


def test_calculation():
    assert almost_equal(core.request('f', {'x': 1, 'y': 2, 'z': 3}), 36.0)
    assert almost_equal(core.request('f', {'x': -1, 'y': -2, 'z': -3}), 36.0)
    assert almost_equal(core.request('f', {'x': 2, 'y': 2, 'z': 2}), 24.0)


def test_derivatives():
    assert almost_equal(core.request('df_x', {'x': 3, 'y': 2, 'z': 3}), 6.0)
    assert almost_equal(core.request('df_y', {'x': 1, 'y': -2, 'z': 3}), -8.0)
    assert almost_equal(core.request('df_z', {'x': 1, 'y': 2, 'z': 11}), 66.0)


def test_gradient():
    grad = core.request('df_grad', {'z': 11, 'x': 3, 'y': -2})
    assert almost_equal(grad[0], 6.0)
    assert almost_equal(grad[1], -8.0)
    assert almost_equal(grad[2], 66.0)


os.remove('temp.json')
