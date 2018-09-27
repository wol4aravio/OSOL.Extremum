from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import *
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class RandomSearch(Algorithm):

    def __init__(self, radius):
        self._x = None
        self._f_x = None
        self._radius = radius

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['radius'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['RandomSearch'])

    def to_dict(self):
        return {
            'radius': self._radius
        }

    def to_json(self):
        return {'RandomSearch': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x}

    @property
    def iterations(self):
        return [self.generate_new_point]

    def initialize(self, f, area, seed):
        if seed is None:
            self._x = generate_random_point_in_rectangular(area)
            self._f_x = f(self._x)
        else:
            if isinstance(seed, list):
                self._x = sorted(seed, key=lambda v: f(v))[0]
                self._f_x = f(self._x)
            else:
                self._x = seed
                self._f_x = f(self._x)

    def generate_new_point(self, f, area):
        x = self._x
        f_x = self._f_x

        x_new = generate_random_point_in_sphere(x, self._radius, area)
        f_x_new = f(x_new)

        if f_x_new < f_x:
            self._x = x_new
            self._f_x = f_x_new

        return self.generate_new_point
