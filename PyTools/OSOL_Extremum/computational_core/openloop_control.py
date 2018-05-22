from OSOL_Extremum.cybernatics.dynamic_system import DynamicSystem
from OSOL_Extremum.arithmetics.interval import Interval
import json
import numpy as np
import pandas as pd
import os


class OpenloopControl:

    def __init__(self, ds):
        self.ds = ds

    def sim(self, parameters):
        times, states, controls, I_integral, I_terminal, error_terminal_state, phase_errors = self.ds.simulate(parameters)
        return sum(I_integral) + I_terminal + sum(error_terminal_state) + sum(phase_errors)

    @staticmethod
    def convert_real_vector(dict):
        v = {}
        for kvp in dict['RealVector']['elements']:
            v[kvp['key']] = float(kvp['value'])
        return v

    @staticmethod
    def convert_interval_vector(dict):
        v = {}
        for kvp in dict['IntervalVector']['elements']:
            v[kvp['key']] = Interval.from_dict(kvp['value'])
        return v

    def outer_sim(self, parameters):
        json_file = parameters['json_file']
        save_loc = parameters['save_loc']
        j = json.load(open(json_file, 'r'))
        if 'RealVector' in j:
            parameters = OpenloopControl.convert_real_vector(j)
        elif 'IntervalVector' in j:
            parameters = OpenloopControl.convert_interval_vector(j)
        else:
            raise Exception('Unsupported data')
        times, states, controls, I_integral, I_terminal, errors_terminal_state, phase_errors = self.ds.simulate(parameters)

        data_state = np.ndarray(shape=(len(times), 1 + len(states[0])))
        cols_state = ['t'] + self.ds.state_vars[:(len(self.ds.state_vars) - len(self.ds.integral_criteria) - len(self.ds.phase_constraints))]
        data_state[:, 0] = times
        for i in range(len(states)):
            data_state[i, 1:] = [states[i][n] for n in cols_state[1:]]
        data_state = pd.DataFrame(data=data_state, columns=cols_state)

        data_control = np.ndarray(shape=(len(controls), 1 + len(controls[0])))
        data_control[:, 0] = times[:-1]
        cols_control = ['t'] + self.ds.control_vars
        for i in range(len(controls)):
            data_control[i, 1:] = [controls[i][n] for n in self.ds.control_vars]
        data_control = pd.DataFrame(data=data_control, columns=cols_control)

        criteria_info = {
            'I_integral': I_integral,
            'I_terminal': I_terminal,
            'errors_terminal_state': errors_terminal_state,
            'phase_errors': phase_errors
        }

        if not os.path.exists(save_loc):
            os.makedirs(save_loc)
        data_state.to_csv(save_loc + '/state.csv', index=False)
        data_control.to_csv(save_loc + '/control.csv', index=False)
        json.dump(criteria_info, open(save_loc + '/criteria.json', 'w'), indent=4)

        return True

    @classmethod
    def from_dict(cls, data):
        return cls(DynamicSystem.from_dict(data))