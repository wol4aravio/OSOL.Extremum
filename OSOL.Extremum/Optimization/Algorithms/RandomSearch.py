from Optimization.Algorithms.Algorithm import Algorithm
from Numerical_Objects.Vector import Vector

import numpy as np


class RandomSearch(Algorithm):

    @staticmethod
    def generate_random_point_in_sphere(current_point, radius, area):
        normally_distributed = Vector({k: v for k, v in zip(area.keys(), np.random.normal(0.0, 1.0, len(area)))})
        length = np.sqrt(sum(np.array(normally_distributed.values) ** 2))
        shift = (np.random.uniform(0.0, radius) / length) * normally_distributed
        return (current_point + shift).constrain(area)

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

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x}

    @property
    def iterations(self):
        return [self.generate_new_points]

    def initialize(self, f, area, seed):
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

    def generate_new_points(self, f, area):
        x = self._x
        f_x = self._f_x

        x_new = RandomSearch.generate_random_point_in_sphere(x, self._radius, area)
        f_x_new = f(x_new)

        if f_x_new < f_x:
            self._x = x_new
            self._f_x = f_x_new

        return self.generate_new_points
