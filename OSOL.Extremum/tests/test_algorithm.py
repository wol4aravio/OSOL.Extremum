from Optimization.Algorithm import Algorithm
from Optimization.Verifier import Verifier
from Numerical_Objects.Interval import Interval
from Numerical_Objects.Vector import Vector

import numpy as np
import logging
logging.basicConfig(level=logging.INFO)


class Dummy_Optimization(Algorithm):
    def __init__(self, N, ratio):
        self.best = None
        self.points = None
        self.delta_area = None
        self.ratio = ratio
        self.N = N

    @property
    def current_state(self):
        return {'result': self.best}

    @property
    def iterations(self):
        return [self.generate_new_points]

    def initialize(self, f, area, seed):
        self.points = []
        for i in range(self.N):
            point = {}
            for k, (left, right) in area.items():
                if np.random.uniform(-1.0, 1.0) < 0.0:
                    point[k] = np.random.uniform(left, right)
                else:
                    [p1, p2] = sorted(np.random.uniform(left, right, (1, 2))[0])
                    point[k] = Interval.create_valid_interval(lower_bound=p1, upper_bound=p2)
            self.points.append(Vector(point))
        self.points = sorted(self.points, key=lambda x: f(x))
        self.best = self.points[0]

        self.delta_area = {}
        for k, (left, right) in area.items():
            shift = self.ratio * (right - left)
            self.delta_area[k] = (-shift, shift)

    def generate_new_points(self, f, area):
        new_points = []
        for x in self.points[1:]:
            delta = {k: np.random.uniform(left, right) for k, (left, right) in self.delta_area.items()}
            new_points += (x >> delta).bisect()
        self.points = sorted(new_points + self.best.bisect(), key=lambda v: f(v))[:self.N]
        self.best = self.points[0]
        return self.generate_new_points


a1 = Dummy_Optimization(5, 0.01)
a2 = Dummy_Optimization(10, 0.005)
a3 = Dummy_Optimization(25, 0.001)

tester = Verifier()


def test_algorithm():
    logger = logging.getLogger('Integration test of optimization parts')
    assert tester.verify([a1, a2, a3], logger)
    print('Done!\n')
