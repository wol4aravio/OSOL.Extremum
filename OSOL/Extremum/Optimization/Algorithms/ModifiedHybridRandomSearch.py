from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class ModifiedHybridRandomSearch(Algorithm):

    def __init__(self, algorithms, terminators):
        self._x = None
        self._f_x = None
        self._algorithms = algorithms
        self._terminators = terminators

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['algorithms'], dict_data['terminators'])

    @classmethod
    def from_json(cls, json_data):
        data = json_data['ModifiedHybridRandomSearch']
        data['algorithms'] = [OSOL.Extremum.Tools.OptimizationTools.create_algorithm_from_json(j) for j in data['algorithms']]
        data['terminators'] = [MaxTimeTerminator.from_json(j) for j in data['terminators']]
        return cls.from_dict(data)

    def to_dict(self):
        return {
            'algorithms': [a.to_json() for a in self._algorithms],
            'terminators': [t.to_json() for t in self._terminators]
        }

    def to_json(self):
        return {'ModifiedHybridRandomSearch': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._x, 'efficiency': self._f_x}

    @property
    def iterations(self):
        return [self.make_one_run]

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

    def make_one_run(self, f, area):
        x = self._x
        f_x = self._f_x

        x_new = self._algorithms[0].work(f, area, self._terminators[0], seed=x)
        for a, t in zip(self._algorithms[1:], self._terminators[1:]):
            x_new = a.work(f, area, t, seed=x_new)
        f_x_new = f(x_new)

        if f_x_new < f_x:
            self._x = x_new
            self._f_x = f_x_new

        return self.make_one_run


import OSOL.Extremum.Tools.OptimizationTools
