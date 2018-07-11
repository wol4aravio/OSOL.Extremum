from Optimization.Algorithms.Algorithm import Algorithm
from Numerical_Objects.Vector import Vector

import numpy as np


class SimulatedAnnealing(Algorithm):

    def __init__(self, init_temperature, C, beta):
        self._x = None
        self._f_x = None
        self._T = None
        self._init_temperature = init_temperature
        self._C = C
        self._beta = beta

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['init_temperature'], dict_data['C'], dict_data['beta'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['SimulatedAnnealing'])

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x, 'temperature': self._T}

    @property
    def iterations(self):
        return [self.generate_new_point]

    def initialize(self, f, area, seed):
        self._T = self._init_temperature
        if seed is None:
            point = {}
            for k, (left, right) in area.items():
                point[k] = np.random.uniform(left, right)
            point = Vector(point)
            self._x = point
            self._f_x = f(point)
        else:
            if type(seed) == list:
                self._x = sorted(seed, key=lambda v: f(v))[0]
                self._f_x = f(self._x)
            else:
                self._x = seed
                self._f_x = f(self._x)

    def generate_new_point(self, f, area):
        x = self._x
        f_x = self._f_x
        T = self._T

        delta = dict(zip(x.keys, np.random.multivariate_normal(mean=np.zeros(shape=(len(x), )),
                                                               cov=T*np.identity(len(x)))))

        x_new = (x >> delta).constrain(area)
        f_x_new = f(x_new)

        if f_x_new < f_x:
            self._x = x_new
            self._f_x = f_x_new
        else:
            bias = np.exp((f_x - f_x_new) / (self._C * self._T))
            if np.random.uniform(0.0, 1.0) < bias:
                self._x = x_new
                self._f_x = f_x_new

        self._T *= self._beta
        return self.generate_new_point
