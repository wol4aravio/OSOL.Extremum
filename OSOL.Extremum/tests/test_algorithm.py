from Optimization.Algorithm import Algorithm
from Optimization.Tester import Tester
from Numerical_Objects.Interval import Interval
from Numerical_Objects.Vector import Vector

import numpy as np


class Dummy_Optimization(Algorithm):
    def __init__(self, ratio):
        self.x = None
        self.delta_area = None
        self.ratio = ratio

    @property
    def current_state(self):
        return {'result': self.x}

    @property
    def iterations(self):
        return [self.generate_new_points]

    def initialize(self, f, area, seed):
        if seed is not None:
            if type(seed) == list:
                self.x = min(seed, key=lambda v: f(v))
            else:
                self.x = seed
        else:
            point = {}
            for k, (left, right) in area.items():
                if np.random.uniform(-1.0, 1.0) < 0.0:
                    point[k] = np.random.uniform(left, right)
                else:
                    [p1, p2] = sorted(np.random.uniform(left, right, (1, 2))[0])
                    point[k] = Interval.create_valid_interval(lower_bound=p1, upper_bound=p2)
            self.x = Vector(point)

        self.delta_area = {}
        for k, (left, right) in area.items():
            shift = self.ratio * (right - left)
            self.delta_area[k] = (-shift, shift)

    def generate_new_points(self, f, area):
        x = self.x
        delta = {k: np.random.uniform(left, right) for k, (left, right) in self.delta_area.items()}
        [x1, x2] = x.bisect()
        [x3, x4] = (x >> delta).bisect()
        self.x = sorted([x1, x2, x3, x4], key=lambda v: f(v))[0]
        return self.generate_new_points


a1 = Dummy_Optimization(0.01)
a2 = Dummy_Optimization(0.005)
a3 = Dummy_Optimization(0.001)

tester = Tester()


def test_algorithm():
    assert tester.test([a1, a2, a3])
