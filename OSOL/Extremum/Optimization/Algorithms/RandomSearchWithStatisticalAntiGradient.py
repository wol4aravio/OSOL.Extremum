from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import generate_random_point_in_sphere
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class RandomSearchWithStatisticalAntiGradient(Algorithm):

    def __init__(self, radius, number_of_samples):
        self._x = None
        self._f_x = None
        self._radius = radius
        self._number_of_samples = number_of_samples

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['radius'], dict_data['number_of_samples'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['RandomSearchWithStatisticalAntiGradient'])

    def to_dict(self):
        return {
            'radius': self._radius,
            'number_of_samples': self._number_of_samples
        }

    def to_json(self):
        return {'RandomSearchWithStatisticalAntiGradient': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x}

    @property
    def iterations(self):
        return [self.generate_new_point]

    def initialize(self, f, area, seed):
        if seed is None:
            point = {}
            for k, (left, right) in area.items():
                point[k] = np.random.uniform(left, right)
            point = Vector(point)
            self._x = point
            self._f_x = f(point)
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
        radius = self._radius
        N = self._number_of_samples

        new_points = []
        new_values = []
        for i in range(N):
            new_points.append(generate_random_point_in_sphere(x, radius, area))
            new_values.append(f(new_points[-1]))

        anti_gradient = Vector({k: 0.0 for k in x.keys})
        for i in range(N):
            anti_gradient -= new_points[i] * (new_values[i] - f_x)
        anti_gradient *= (1.0 / anti_gradient.length)

        x_new = x + np.random.uniform(0.0, radius) * anti_gradient
        f_x_new = f(x_new)

        if f_x_new < f_x:
            self._x = x_new
            self._f_x = f_x_new

        return self.generate_new_point
