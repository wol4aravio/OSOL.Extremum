from Tools.Encoders import CustomEncoder
from Cybernatics.DynamicSystem import DynamicSystem
from Optimization.Tasks.OpenloopControl import OpenloopControl
from Numerical_Objects.Vector import Vector
from Numerical_Objects.Interval import Interval
from tests.test_dynamic_system import ds_json

import json
import os
import shutil
import math


ds = DynamicSystem.from_dict(json.loads(ds_json))
task = OpenloopControl(ds)


def test_real():

    tol = 1e-3
    I_integral_ideal = [0.77272105923056, 46.639683900497, 6.80452330242669]
    I_terminal_ideal = 8.99891199975
    phase_errors_ideal = [34784.1137839443, 5.62296778644782e-07, 0.0]
    controller_variance_ideal = [4.0, 0.0, 0.0]
    terminal_error = 1e-3

    parameters = {
        'u1_0': 5,
        'u1_1': 6,
        'u1_2': 7,

        'u2_0': 2,
        'u2_1': 2,
        'u2_2': 2,
        'u2_3': 2,

        'a': 5
    }

    error = task(parameters)

    assert math.fabs(error - (sum(I_integral_ideal) + I_terminal_ideal + terminal_error + sum(phase_errors_ideal) + sum(controller_variance_ideal))) < tol


def test_interval():

    tol = 1e-3
    I_integral_ideal = [0.77272105923056, 46.639683900497, 6.80452330242669]
    I_terminal_ideal = 8.99891199975
    phase_errors_ideal = [34784.1137839443, 5.62296778644782e-07, 0.0]
    controller_variance_ideal = [4.0, 0.0, 0.0]
    terminal_error = 1e-3

    parameters = {
        'u1_0': Interval.from_value(5),
        'u1_1': Interval.from_value(6),
        'u1_2': Interval.from_value(7),

        'u2_0': Interval.from_value(2),
        'u2_1': Interval.from_value(2),
        'u2_2': Interval.from_value(2),
        'u2_3': Interval.from_value(2),

        'a': Interval.from_value(5)
    }

    error = task(parameters)

    assert math.fabs(error - (sum(I_integral_ideal) + I_terminal_ideal + terminal_error + sum(phase_errors_ideal) + sum(controller_variance_ideal))) < tol


def test_outer():
    parameters = {
        'u1_0': 5,
        'u1_1': 6,
        'u1_2': 7,
        'u2_0': 2,
        'u2_1': 2,
        'u2_2': 2,
        'u2_3': 2,
        'a': 5
    }

    os.makedirs('temp')
    json.dump(Vector(parameters), open('temp/p.json', 'w'), cls=CustomEncoder, indent=2)
    from_json = task.outer_sim('temp/p.json', 'test')
    shutil.rmtree('temp')
    shutil.rmtree('test')

    assert from_json
