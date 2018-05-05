import os
from math import fabs

from OSOL_Extremum.computational_core.unconstrained_optimization import *

file_writer = open('temp.json', 'w')
file_writer.writelines(
    """
{
	"f": "x ** 2 + y ** 2 + z ** 2",
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
}
    """)
file_writer.close()

task = UnconstrainedOptimization.from_json('temp.json')

tol = 1e-7


def almost_equal(v1, v2):
    return fabs(v1 - v2) < tol


def test_calculation():
    assert almost_equal(task.f(1, 2, 3), 14.0)
    assert almost_equal(task.f(-1, -2, -3), 14.0)
    assert almost_equal(task.f(2, 2, 2), 12.0)


def test_derivatives():
    assert almost_equal(task.df['x'](3, 2, 3), 6.0)
    assert almost_equal(task.df['y'](1, -2, 3), -4.0)
    assert almost_equal(task.df['z'](1, 2, 11), 22.0)


def test_gradient():
    grad = task.df['grad'](3, -2, 11)
    assert almost_equal(grad[0], 6.0)
    assert almost_equal(grad[1], -4.0)
    assert almost_equal(grad[2], 22.0)


os.remove('temp.json')
