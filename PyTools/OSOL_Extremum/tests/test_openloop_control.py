import os
import math

from OSOL_Extremum.computational_core.computational_core import *
from OSOL_Extremum.arithmetics.interval import Interval


resource_loc = os.environ.get('RESOURCE_LOC')
if resource_loc is None:
    resource_loc = 'resources/cybernatics_1.json'
else:
    resource_loc = '{}/resources/cybernatics_1.json'.format(resource_loc)

core = ComputationalCore.from_json(resource_loc)


def test_real():

    tol = 1e-3
    I_integral_ideal = 54.2169282621542
    I_terminal_ideal = 8.99891199975
    phase_errors_ideal = [34784.1137839443, 5.62296778644782e-07, 0.0]

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

    error = core.request('sim', parameters)

    assert math.fabs(error - (I_integral_ideal + I_terminal_ideal + sum(phase_errors_ideal))) < tol


def test_interval():

    tol = 1e-3
    I_integral_ideal = 54.2169282621542
    I_terminal_ideal = 8.99891199975
    phase_errors_ideal = [34784.1137839443, 5.62296778644782e-07, 0.0]

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

    error = core.request('sim', parameters).middle_point

    assert math.fabs(error - (I_integral_ideal + I_terminal_ideal + sum(phase_errors_ideal))) < tol