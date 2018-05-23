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

    error = core.request('sim', parameters)

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

    error = core.request('sim', parameters).middle_point

    assert math.fabs(error - (sum(I_integral_ideal) + I_terminal_ideal + terminal_error + sum(phase_errors_ideal) + sum(controller_variance_ideal))) < tol


def test_outer():
    parameters_json = {
        'RealVector': {
            'elements': [
                {
                    'key': 'u1_0',
                    'value': 5
                },
                {
                    'key': 'u1_1',
                    'value': 6
                },
                {
                    'key': 'u1_2',
                    'value': 7
                },

                {
                    'key': 'u2_0',
                    'value': 2
                },
                {
                    'key': 'u2_1',
                    'value': 2
                },
                {
                    'key': 'u2_2',
                    'value': 2
                },
                {
                    'key': 'u2_3',
                    'value': 2
                },

                {
                    'key': 'a',
                    'value': 5
                }
            ]
        }
    }
    os.makedirs('temp')
    json.dump(parameters_json, open('temp/p.json', 'w'))
    from_json = core.request('sim_out', {'json_file': 'temp/p.json', 'save_loc': 'test'})
    os.remove('temp/p.json')
    os.remove('test/state.csv')
    os.remove('test/control.csv')
    os.remove('test/criteria.json')
    os.rmdir('temp')
    os.rmdir('test')

    assert from_json
