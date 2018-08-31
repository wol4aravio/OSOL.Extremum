from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import generate_random_point_in_rectangular
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class DolphinSwarm(Algorithm):

    def __init__(self, number_of_dolphins, speed, search_time, number_of_directions):
        self._dolphins = None
        self._dolphins_K = None
        self._dolphins_L = None
        self._dolphins_K_fit = None
        self._dolphins_L_fit = None

        self._number_of_dolphins = number_of_dolphins
        self._speed = speed
        self._search_time = search_time
        self._number_of_directions = number_of_directions

    @classmethod
    def from_dict(cls, dict_data):
        return cls(
            dict_data['number_of_dolphins'],
            dict_data['speed'],
            dict_data['search_time'],
            dict_data['number_of_directions'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['DolphinSwarm'])

    def to_dict(self):
        return {
            'number_of_dolphins': self._number_of_dolphins,
            'speed': self._speed,
            'search_time': self._search_time,
            'number_of_directions': self._number_of_directions
        }

    def to_json(self):
        return {'DolphinSwarm': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._refresh_best_dolphin(), 'dolphins_K': self._dolphins_K}

    @property
    def iterations(self):
        return [self.search_phase]

    def _refresh_best_dolphin(self):
        min_id = np.argmin(self._dolphins_K_fit)
        return self._dolphins_K[min_id]

    def initialize(self, f, area, seed):
        if seed is None:
            for i in range(self._number_of_dolphins):
                self._dolphins.append(generate_random_point_in_rectangular(area))
        else:
            if isinstance(seed, list):
                self._dolphins = sorted(seed, key=lambda v: f(v))[:self._number_of_dolphins]
            else:
                self._dolphins = seed
            if len(self._dolphins) < self._number_of_dolphins:
                for i in range(len(self._dolphins), self._number_of_dolphins):
                    self._dolphins.append(generate_random_point_in_rectangular(area))

        self._dolphins_K = [d.copy() for d in self._dolphins]
        self._dolphins_K_fit = [f(d) for d in self._dolphins_K]
        return

    def search_phase(self, f, area):
        self._dolphins_L = []
        self._dolphins_L_fit = []
        for d_id, d in enumerate(self._dolphins):
            velocities = [generate_random_point_in_rectangular({k: (-1.0, 1.0) for k in area.keys})
                          for _ in range(self._number_of_directions)]
            investigated_locations = [d + v * i for v in velocities for i in range(1, self._search_time + 1)]
            fitness = [f(loc) for loc in investigated_locations]
            best_loc_id = np.argmin(fitness)
            self._dolphins_L.append(investigated_locations[best_loc_id])
            self._dolphins_L_fit.append(fitness[best_loc_id])
            if self._dolphins_L_fit[d_id] < self._dolphins_K_fit[d_id]:
                self._dolphins_K_fit[d_id] = self._dolphins_L_fit[d_id]
                self._dolphins_K = self._dolphins_L[d_id].copy()
        return

