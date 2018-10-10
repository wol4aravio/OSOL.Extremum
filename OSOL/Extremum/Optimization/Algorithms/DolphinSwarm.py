from OSOL.Extremum.Optimization.Algorithms.Algorithm import Algorithm
from OSOL.Extremum.Optimization.Algorithms.tools import *
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import numpy as np


class DolphinSwarm(Algorithm):

    def __init__(self,
                 number_of_dolphins, speed, search_time,
                 number_of_directions, acceleration, maximum_transmission_time,
                 radius_reduction_coefficient):
        self._dolphins = None
        self._dolphins_K = None
        self._dolphins_L = None
        self._dolphins_K_fit = None
        self._dolphins_L_fit = None

        self._number_of_dolphins = number_of_dolphins
        self._speed = speed
        self._search_time = search_time
        self._number_of_directions = number_of_directions
        self._acceleration = acceleration
        self._maximum_transmission_time = maximum_transmission_time
        self._radius_reduction_coefficient = radius_reduction_coefficient

        self._transmission_time_matrix = np.full(
            shape=(number_of_dolphins, number_of_dolphins),
            fill_value=np.inf)

    @classmethod
    def from_dict(cls, dict_data):
        return cls(
            dict_data['number_of_dolphins'],
            dict_data['speed'],
            dict_data['search_time'],
            dict_data['number_of_directions'],
            dict_data['acceleration'],
            dict_data['maximum_transmission_time'],
            dict_data['radius_reduction_coefficient'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['DolphinSwarm'])

    def to_dict(self):
        return {
            'number_of_dolphins': self._number_of_dolphins,
            'speed': self._speed,
            'search_time': self._search_time,
            'number_of_directions': self._number_of_directions,
            'acceleration': self._acceleration,
            'maximum_transmission_time': self._maximum_transmission_time,
            'radius_reduction_coefficient': self._radius_reduction_coefficient
        }

    def to_json(self):
        return {'DolphinSwarm': self.to_dict()}

    @property
    def current_state(self):
        return {'result': self._refresh_best_dolphin(), 'dolphins_K': self._dolphins_K}

    @property
    def iterations(self):
        return [self.search_phase, self.call_phase, self.predation_phase]

    def _refresh_best_dolphin(self):
        min_id = np.argmin(self._dolphins_K_fit)
        return self._dolphins_K[min_id]

    def initialize(self, f, area, seed):
        self._dolphins = []
        if seed is None:
            for _ in range(self._number_of_dolphins):
                self._dolphins.append(generate_random_point_in_rectangular(area))
        else:
            if isinstance(seed, list):
                self._dolphins = sorted(seed, key=f)[:self._number_of_dolphins]
            else:
                self._dolphins = seed
            if len(self._dolphins) < self._number_of_dolphins:
                for i in range(len(self._dolphins), self._number_of_dolphins):
                    self._dolphins.append(generate_random_point_in_rectangular(area))

        self._dolphins_K = [d.copy() for d in self._dolphins]
        self._dolphins_K_fit = [f(d) for d in self._dolphins_K]
        return

    def search_phase(self, f, area):
        speed = self._speed
        self._dolphins_L = []
        self._dolphins_L_fit = []
        for d_id, d in enumerate(self._dolphins):
            velocities = [generate_random_point_in_rectangular({k: (-1.0, 1.0) for k in area.keys()})
                          for _ in range(self._number_of_directions)]
            velocities = [v * (speed / v.length) for v in velocities]
            investigated_locations = [d + v * i for v in velocities for i in range(1, self._search_time + 1)]
            investigated_locations = [loc.constrain(area) for loc in investigated_locations]
            fitness = [f(loc) for loc in investigated_locations]
            best_loc_id = np.argmin(fitness)
            self._dolphins_L.append(investigated_locations[best_loc_id])
            self._dolphins_L_fit.append(fitness[best_loc_id])
            if self._dolphins_L_fit[d_id] < self._dolphins_K_fit[d_id]:
                self._dolphins_K_fit[d_id] = self._dolphins_L_fit[d_id]
                self._dolphins_K[d_id] = self._dolphins_L[d_id].copy()

        return self.call_phase

    def call_phase(self, f, area):
        N = self._number_of_dolphins
        A = self._acceleration
        speed = self._speed
        T2 = self._maximum_transmission_time
        for i in range(N):
            for j in range(N):
                if self._dolphins_K_fit[j] < self._dolphins_K_fit[i]:
                    distance = distance_between_vectors(self._dolphins_K[i], self._dolphins_K[j])
                    bias = int(np.ceil(distance / (A * speed)))
                    if self._transmission_time_matrix[i, j] > bias:
                        self._transmission_time_matrix[i, j] = bias

        self._transmission_time_matrix -= 1
        for i in range(N):
            for j in range(N):
                if self._transmission_time_matrix[i, j] == 0:
                    self._transmission_time_matrix[i, j] = T2
                    if self._dolphins_K_fit[j] < self._dolphins_K_fit[i]:
                        self._dolphins_K_fit[i] = self._dolphins_K_fit[j]
                        self._dolphins_K[i] = self._dolphins_K[j].copy()

        return self.predation_phase

    @staticmethod
    def _dolphin_movement(area, d, r):
        xi = generate_random_point_in_rectangular({k: (-1.0, 1.0) for k in area.keys()})
        xi *= 1.0 / xi.length
        new_d = (d + xi * r).constrain(area)
        return new_d

    def predation_phase(self, f, area):
        R1 = self._search_time * self._speed
        e = self._radius_reduction_coefficient
        for d_id, d in enumerate(self._dolphins):
            DK = distance_between_vectors(d, self._dolphins_K[d_id])
            DKL = distance_between_vectors(self._dolphins_K[d_id], self._dolphins_L[d_id])

            if DK <= R1:
                R2 = (1.0 - 2.0 / e) * DK
                new_dolphin = self._dolphins_K[d_id] + (d - self._dolphins_K[d_id]) * (R2 / (1e-17 + DK))
            else:
                p_11 = DK / self._dolphins_K_fit[d_id]
                p_12 = (DK - DKL) / self._dolphins_L_fit[d_id]
                p_2 = (e * DK) / (1e-17 + self._dolphins_K_fit[d_id])
                R2 = (1.0 - (p_11 + p_12) / p_2) * DK
                new_dolphin = DolphinSwarm._dolphin_movement(area, self._dolphins_K[d_id], R2)

            new_dolphin_fitness = f(new_dolphin)
            self._dolphins[d_id] = new_dolphin
            if new_dolphin_fitness < self._dolphins_K_fit[d_id]:
                self._dolphins_K_fit[d_id] = new_dolphin_fitness
                self._dolphins_K[d_id] = new_dolphin.copy()

        return self.search_phase
