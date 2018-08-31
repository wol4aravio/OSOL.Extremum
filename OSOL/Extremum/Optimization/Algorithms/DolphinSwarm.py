from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import generate_random_point_in_sphere
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class DolphinSwarm(Algorithm):

    def __init__(self, number_of_dolphins):
        self._dolphins = None
        self._dolphins_K = None
        self._dolphins_K_fit = None

        self._number_of_dolphins = number_of_dolphins

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['number_of_dolphins'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['DolphinSwarm'])

    def to_dict(self):
        return {
            'number_of_dolphins': self._number_of_dolphins
        }

    def to_json(self):
        return {'DolphinSwarm': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._refresh_best_dolphin(), 'dolphins_K': self._dolphins_K}

    # @property
    # def iterations(self):
    #     return [self.generate_new_point]

    def _refresh_best_dolphin(self):
        min_id = np.argmin(self._dolphins_K_fit)
        return self._dolphins_K[min_id]

    def initialize(self, f, area, seed):
        if seed is None:
            for i in range(self._number_of_dolphins):
                self._dolphins.append(Vector({k: np.random.uniform(left, right)
                                              for k, (left, right) in area.items()}))
        else:
            if isinstance(seed, list):
                self._dolphins = sorted(seed, key=lambda v: f(v))[:self._number_of_dolphins]
            else:
                self._dolphins = seed
            if len(self._dolphins) < self._number_of_dolphins:
                for i in range(len(self._dolphins), self._number_of_dolphins):
                    self._dolphins.append(Vector({k: np.random.uniform(left, right)
                                                  for k, (left, right) in area.items()}))

        self._dolphins_K = [d.copy() for d in self._dolphins]
        self._dolphins_K_fit = [f(d) for d in self._dolphins_K]
        return
