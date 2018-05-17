import random

from OSOL_Extremum.cybernatics.controllers import *


def sim(v1, v2, tol=1e-7):
    return v1[0] == v2[0] and np.abs(v1[1] - v2[1]) < tol


def test_PWC():

    switch_points = np.linspace(0.0, 1.0, 11)[:-1]

    params = [('u_{}'.format(i), i) for i in range(0, 10)] + [('k_{}'.format(i), i) for i in range(0, 10)]
    random.shuffle(params)
    controls = dict(params)

    controller = PiecewiseConstantController('u', switch_points, None)
    controller.set_parameters(controls)

    assert sim(controller.get_control(0, x=None), ('u', 0))
    assert sim(controller.get_control(0.32, x=None), ('u', 3))
    assert sim(controller.get_control(0.55, x=None), ('u', 5))
    assert sim(controller.get_control(0.79, x=None), ('u', 7))


def test_PWL():

    switch_points = np.linspace(0.0, 1.0, 11)

    params = [('u_{}'.format(i), i) for i in range(0, 11)] + [('k_{}'.format(i), i) for i in range(0, 11)]
    random.shuffle(params)
    controls = dict(params)

    controller = PiecewiseLinearController('u', switch_points, None)
    controller.set_parameters(controls)

    assert sim(controller.get_control(0, x=None), ('u', 0))
    assert sim(controller.get_control(0.32, x=None), ('u', 3.2))
    assert sim(controller.get_control(0.55, x=None), ('u', 5.5))
    assert sim(controller.get_control(0.79, x=None), ('u', 7.9))


def test_Explicit():

    def real(a, b, t, x):
        return a * np.exp(t) + b * np.exp(-x)

    formula = 'a * exp(t) + b * exp(-x)'
    vars = ['t', 'x']
    param_names = ['a', 'b']

    controller = ExplicitController('u', formula, vars, param_names)
    controller.set_parameters({'a': 1, 'b': 1, 'c': 0})

    assert sim(controller.get_control(0, x={'x': 1, 'y': 77.7}), ('u', real(a=1, b=1, t=0, x=1)))
    assert sim(controller.get_control(7.9, x={'x': 3.0, 'y': -3243.323}), ('u', real(a=1, b=1, t=7.9, x=3.0)))
    assert sim(controller.get_control(1.1, x={'x': -1.21, 'y': 2.1}), ('u', real(a=1, b=1, t=1.1, x=-1.21)))
