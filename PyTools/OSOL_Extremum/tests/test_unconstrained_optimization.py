from math import fabs
import os

from OSOL_Extremum.computational_core.computational_core import *
from OSOL_Extremum.arithmetics.interval import Interval


core = ComputationalCore.from_json('{}/Dummy/Dummy_3.json'.format(os.environ.get('OSOL_EXTREMUM_TASKS_LOC')))

tol = 1e-7


def almost_equal_real(v1, v2):
    return fabs(v1 - v2) < tol


def almost_equal_interval(i1, i2):
    return fabs(i1.lower_bound - i2.lower_bound) + fabs(i1.upper_bound - i2.upper_bound) < 2 * tol


def test_real_calculation():
    assert almost_equal_real(core.request('f', {'x': 1, 'y': 2, 'z': 3}), 36.0)
    assert almost_equal_real(core.request('f', {'x': -1, 'y': -2, 'z': -3}), 36.0)
    assert almost_equal_real(core.request('f', {'x': 2, 'y': 2, 'z': 2}), 24.0)


def test_real_derivatives():
    assert almost_equal_real(core.request('df_x', {'x': 3, 'y': 2, 'z': 3}), 6.0)
    assert almost_equal_real(core.request('df_y', {'x': 1, 'y': -2, 'z': 3}), -8.0)
    assert almost_equal_real(core.request('df_z', {'x': 1, 'y': 2, 'z': 11}), 66.0)


def test_real_gradient():
    grad = core.request('df_grad', {'z': 11, 'x': 3, 'y': -2})
    assert almost_equal_real(grad[0], 6.0)
    assert almost_equal_real(grad[1], -8.0)
    assert almost_equal_real(grad[2], 66.0)


def test_interval_calculation():
    assert almost_equal_interval(core.request('f', {'x': Interval(1, 2), 'y': Interval(2, 3), 'z': Interval(3, 4)}), Interval(36.0, 70.0))


def test_interval_derivatives():
    assert almost_equal_interval(core.request('df_x',
                                              {'x': Interval(3, 4),
                                               'y': Interval.from_value(2),
                                               'z': Interval.from_value(3)}),
                                 Interval(6, 8))
    assert almost_equal_interval(core.request('df_y',
                                              {'x': Interval.from_value(1),
                                               'y': Interval(-2, 1),
                                               'z': Interval.from_value(3)}),
                                 Interval(-8, 4))
    assert almost_equal_interval(core.request('df_z',
                                              {'x': Interval.from_value(1),
                                               'y': Interval.from_value(2),
                                               'z': Interval.from_value(11)}),
                                 Interval.from_value(66.0))


def test_interval_gradient():
    grad = core.request('df_grad', {'z': Interval.from_value(11), 'x': Interval(3, 4), 'y': Interval(-2, 1)})
    assert almost_equal_interval(grad[0], Interval(6, 8))
    assert almost_equal_interval(grad[1], Interval(-8, 4))
    assert almost_equal_interval(grad[2], Interval.from_value(66.0))
