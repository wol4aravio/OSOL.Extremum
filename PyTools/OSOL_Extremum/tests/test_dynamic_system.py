from OSOL_Extremum.cybernatics.dynamic_system import DynamicSystem
from OSOL_Extremum.arithmetics.interval import Interval

import numpy as np
import sklearn.metrics.regression as RM


def rmse(x, y):
    return np.sqrt(RM.mean_squared_error(x, y))


# simple ds: x' = 2*t
def test_1():
    tol = 1e-3

    ds = DynamicSystem(sampling_type='Euler', sampling_eps=1e-3, sampling_max_steps=1000000,
                       f={'x': '2*t'}, state_vars=['x'], initial_conditions={'x': 0},
                       controllers={}, control_vars=[], control_bounds={},
                       aux={}, etc_vars=[],
                       integral_criterion='0', terminal_criterion='0',
                       terminal_constraints=[{'equation': 't - 1.0', 'max_error': 1e-5, 'penalty': 1e+5, 'norm': 'L2'}], phase_constraints=[])
    times = np.linspace(0.0, 1.0, 1000 + 1)
    x_ideal = times * times

    _, x, _ = ds.simulate({})
    x_real = list(map(lambda v: v['x'], x))

    ds.initial_conditions = {'x': Interval.from_value(0.0)}
    _, x, _ = ds.simulate({})
    x_interval = list(map(lambda v: v['x'].middle_point, x))

    error_real = rmse(x_real, x_ideal)
    error_interval = rmse(x_interval, x_ideal)

    assert error_real < tol
    assert error_interval < tol
    assert np.abs(error_real - error_interval < tol * tol)


# simple ds: x' = cos(t)
def test_2():
    tol = 1e-3

    ds = DynamicSystem(sampling_type='RK4', sampling_eps=1e-3, sampling_max_steps=10000,
                       f={'x': 'cos(t)'}, state_vars=['x'], initial_conditions={'x': 0},
                       controllers={}, control_vars=[], control_bounds={},
                       aux={}, etc_vars=[],
                       integral_criterion='0', terminal_criterion='0',
                       terminal_constraints=[], phase_constraints=[])
    times = np.linspace(0.0, ds.sampling_eps * ds.sampling_max_steps, ds.sampling_max_steps + 1)
    x_ideal = np.sin(times)

    _, x, _ = ds.simulate({})
    x_real_RK4 = list(map(lambda v: v['x'], x))

    ds.initial_conditions = {'x': Interval.from_value(0.0)}
    _, x, _ = ds.simulate({})
    x_interval_RK4 = list(map(lambda v: v['x'].middle_point, x))

    error_real_RK4 = rmse(x_real_RK4, x_ideal)
    error_interval_RK4 = rmse(x_interval_RK4, x_ideal)

    ds.sampling_type = 'Euler'
    ds.prolong = ds.prolong_Euler
    ds.initial_conditions = {'x': 0.0}

    _, x, _ = ds.simulate({})
    x_real_Euler = list(map(lambda v: v['x'], x))

    ds.initial_conditions = {'x': Interval.from_value(0.0)}
    _, x, _ = ds.simulate({})
    x_interval_Euler = list(map(lambda v: v['x'].middle_point, x))

    error_real_Euler = rmse(x_real_Euler, x_ideal)
    error_interval_Euler = rmse(x_interval_Euler, x_ideal)

    assert error_real_Euler < tol
    assert error_interval_Euler < tol
    assert np.abs(error_real_Euler - error_interval_Euler < tol * tol)
    assert error_real_RK4 < tol
    assert error_interval_RK4 < tol
    assert np.abs(error_real_RK4 - error_interval_RK4 < tol * tol)
    assert error_real_RK4 < error_real_Euler
    assert error_interval_RK4 < error_interval_Euler


# ode with 2 eqs: x1' = cos(t), x2' = x1
def test_3():
    tol = 2e-3

    ds = DynamicSystem(sampling_type='Euler', sampling_eps=1e-3, sampling_max_steps=10000,
                       f={'x1': 'ct', 'x2': 'x1'}, state_vars=['x1', 'x2'], initial_conditions={'x1': 0, 'x2': -1.0},
                       controllers={}, control_vars=[], control_bounds={},
                       aux={'ct': 'cos(t)'}, etc_vars=['ct'],
                       integral_criterion='0', terminal_criterion='0',
                       terminal_constraints=[], phase_constraints=[])
    times = np.linspace(0.0, ds.sampling_eps * ds.sampling_max_steps, ds.sampling_max_steps + 1)
    x1_ideal = np.sin(times)
    x2_ideal = -np.cos(times)

    _, x, _ = ds.simulate({})
    x1_real_Euler = list(map(lambda v: v['x1'], x))
    x2_real_Euler = list(map(lambda v: v['x2'], x))

    ds.initial_conditions = {'x1': Interval.from_value(0.0), 'x2': Interval.from_value(-1.0)}
    _, x, _ = ds.simulate({})
    x1_interval_Euler = list(map(lambda v: v['x1'].middle_point, x))
    x2_interval_Euler = list(map(lambda v: v['x2'].middle_point, x))

    error_real_Euler = rmse(x1_real_Euler, x1_ideal) + rmse(x2_real_Euler, x2_ideal)
    error_interval_Euler = rmse(x1_interval_Euler, x1_ideal) + rmse(x2_interval_Euler, x2_ideal)

    ds.sampling_type = 'RK4'
    ds.prolong = ds.prolong_RK4
    ds.initial_conditions = {'x1': 0.0, 'x2': -1.0}

    _, x, _ = ds.simulate({})
    x1_real_RK4 = list(map(lambda v: v['x1'], x))
    x2_real_RK4 = list(map(lambda v: v['x2'], x))

    ds.initial_conditions = {'x1': Interval.from_value(0.0), 'x2': Interval.from_value(-1.0)}
    _, x, _ = ds.simulate({})
    x1_interval_RK4 = list(map(lambda v: v['x1'].middle_point, x))
    x2_interval_RK4 = list(map(lambda v: v['x2'].middle_point, x))

    error_real_RK4 = rmse(x1_real_RK4, x1_ideal) + rmse(x2_real_RK4, x2_ideal)
    error_interval_RK4 = rmse(x1_interval_RK4, x1_ideal) + rmse(x2_interval_RK4, x2_ideal)

    assert error_real_Euler < 2 * tol
    assert error_interval_Euler < 2 * tol
    assert np.abs(error_real_Euler - error_interval_Euler < tol * tol)
    assert error_real_RK4 < 2 * tol
    assert error_interval_RK4 < 2 * tol
    assert np.abs(error_real_RK4 - error_interval_RK4 < tol * tol)
    assert error_real_RK4 < error_real_Euler
    assert error_interval_RK4 < error_interval_Euler
