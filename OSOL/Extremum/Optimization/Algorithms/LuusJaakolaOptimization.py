from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import *
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class LuusJaakolaOptimization(Algorithm):

    def __init__(self, init_radius, number_of_samples, reduction_coefficient, recover_coefficient, iteration_per_run):
        self._x = None
        self._f_x = None
        self._radius = None
        self._run_id = None
        self._iteration_id = None
        self._init_radius = init_radius
        self._number_of_samples = number_of_samples
        self._reduction_coefficient = reduction_coefficient
        self._recover_coefficient = recover_coefficient
        self._iteration_per_run = iteration_per_run

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['init_radius'],
                   dict_data['number_of_samples'],
                   dict_data['reduction_coefficient'],
                   dict_data['recover_coefficient'],
                   dict_data['iteration_per_run'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['LuusJaakolaOptimization'])

    def to_dict(self):
        return {
            'init_radius': self._init_radius,
            'number_of_samples': self._number_of_samples,
            'reduction_coefficient': self._reduction_coefficient,
            'recover_coefficient': self._recover_coefficient,
            'iteration_per_run': self._iteration_per_run
        }

    def to_json(self):
        return {'LuusJaakolaOptimization': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x, 'radius': self._radius}

    @property
    def iterations(self):
        return [self.initialize_radius_on_run,
                self.generate_new_point,
                self.check_run_termination]

    def initialize(self, f, area, seed):
        self._run_id = 0
        self._iteration_id = 0
        if seed is None:
            self._x = generate_random_point_in_rectangular(area)
            self._f_x = f(self._x)
        else:
            self._x = get_best_point_from_seed(seed)
            self._f_x = f(self._x)

    def initialize_radius_on_run(self, f, area):
        self._radius = np.power(self._recover_coefficient, self._run_id) * self._init_radius
        return self.generate_new_point

    def generate_new_point(self, f, area):
        x = self._x
        f_x = self._f_x

        for _ in range(self._number_of_samples):
            x_new = generate_random_point_in_sphere(x, self._radius, area)
            f_x_new = f(x_new)

            if f_x_new < f_x:
                self._x = x_new
                self._f_x = f_x_new

        self._radius *= self._reduction_coefficient
        self._iteration_id += 1
        return self.check_run_termination

    def check_run_termination(self, f, area):
        if self._iteration_id == self._iteration_per_run:
            self._iteration_id = 0
            self._run_id += 1
            return self.initialize_radius_on_run
        else:
            return self.generate_new_point
