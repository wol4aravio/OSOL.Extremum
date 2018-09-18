from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import generate_random_point_in_sphere
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class GradientDescent(Algorithm):

    def __init__(self, alpha):
        self._x = None
        self._f_x = None
        self._grad = None
        self._alpha = alpha

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['alpha'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['GradientDescent'])

    def to_dict(self):
        return {
            'alpha': self._alpha
        }

    def to_json(self):
        return {'GradientDescent': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x}

    @property
    def iterations(self):
        return [self.make_step]

    def renew_grad(self):
        self._f_x.backward(retain_graph=True)
        self._grad = self._x.grad()

    def initialize(self, f, area, seed):
        if seed is None:
            point = {}
            for k, (left, right) in area.items():
                point[k] = np.random.uniform(left, right)
            point = Vector(point)
            self._x = point
            self._x.to_pytorch_vector()
            self._f_x = f(point)
        else:
            if isinstance(seed, list):
                self._x = sorted(seed, key=lambda v: f(v))[0]
            else:
                self._x = seed
            self._x.to_pytorch_vector()
            self._f_x = f(self._x)
        self.renew_grad()


    def make_step(self, f, area):
        print(self._x, self._grad)
        self._x = self._x - self._alpha * self._grad
        self._x = self._x.constrain(area)
        self._f_x = f(self._x)
        self.renew_grad()

        return self.make_step
