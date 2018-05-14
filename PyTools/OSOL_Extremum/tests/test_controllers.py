import pytest
import numpy as np

from OSOL_Extremum.cybernatics.controllers import *


def test_PWC():
    switch_points = np.linspace(0.0, 1.0, 11)[:-1]
    controls = range(0, 10)
    controller = PiecewiseConstantController(switch_points, controls)

    assert controller.get_control(0, x=None) == 0
    assert controller.get_control(0.32, x=None) == 3
    assert controller.get_control(0.55, x=None) == 5
    assert controller.get_control(0.79, x=None) == 7


def test_PWL():

    def sim(v1, v2, tol=1e-7):
        return np.abs(v1 - v2) < tol

    switch_points = np.linspace(0.0, 1.0, 11)
    controls = range(0, 11)
    controller = PiecewiseLinearController(switch_points, controls)

    assert sim(controller.get_control(0, x=None), 0)
    assert sim(controller.get_control(0.32, x=None), 3.2)
    assert sim(controller.get_control(0.55, x=None), 5.5)
    assert sim(controller.get_control(0.79, x=None), 7.9)
