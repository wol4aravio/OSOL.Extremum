from Optimization.Algorithms.Algorithm import Algorithm
from Numerical_Objects.Vector import Vector
from Numerical_Objects.Interval import Interval

import numpy as np


class Bomb:
    def __init__(self, location):
        self._location = location
        self._efficiency = None

    def get_efficiency(self, f):
        self._efficiency = f(self._location)

    def explode(self, f, area, power):
        split_component = self._location.get_widest_component()
        [part_left, part_right] = self._location.bisect(key=split_component)

        shift_left = {}
        shift_right = {}
        for k, (min_value, max_value) in power.items():
            if k != split_component:
                shift_left[k] = np.random.uniform(min_value, max_value)
                shift_right[k] = np.random.uniform(min_value, max_value)
            else:
                shift_left[k] = np.random.uniform(min_value, 0.0)
                shift_right[k] = np.random.uniform(0.0, max_value)

        part_left = Bomb((part_left >> shift_left).constrain(area))
        part_right = Bomb((part_right >> shift_right).constrain(area))

        part_left.get_efficiency(f)
        part_right.get_efficiency(f)

        return [part_left, part_right]


class IntervalExplosionSearch(Algorithm):

    def __init__(self, max_bombs, max_radius_ratio):
        self._max_bombs = max_bombs
        self._max_radius_ratio = max_radius_ratio
        self._bombs = None
        self._deltas = None

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['max_bombs'], dict_data['max_radius_ratio'])

    @classmethod
    def from_json(cls, json_data):
        return cls.from_dict(json_data['IntervalExplosionSearch'])

    def to_dict(self):
        return {
            'max_bombs': self._max_bombs,
            'max_radius_ratio': self._max_radius_ratio
        }

    def to_json(self):
        return {'IntervalExplosionSearch': self.to_dict}

    @property
    def current_state(self):
        return {'bombs': self._bombs,
                'result': self._bombs[0]._location}

    @property
    def iterations(self):
        return [
            self.calculate_deltas,
            self.generate_new_bombs
        ]

    def initialize(self, f, area, seed):
        self._bombs = []
        if seed is None:
            for i in range(self._max_bombs):
                point = {}
                for k, (left, right) in area.items():
                    [p1, p2] = sorted(np.random.uniform(left, right, (1, 2))[0])
                    point[k] = Interval.create_valid_interval(lower_bound=p1, upper_bound=p2)
                self._bombs.append(Bomb(Vector(point)))
        else:
            while len(self._bombs) < self._max_bombs:
                if isinstance(seed, list):
                    self._bombs += [Bomb(v) for v in seed]
                else:
                    self._bombs += [Bomb(seed)]
            self._bombs = self._bombs[:self._max_bombs]

        for i in range(self._max_bombs):
            self._bombs[i].get_efficiency(f)
        self._bombs = sorted(self._bombs, key=lambda b: b._efficiency)

    def calculate_deltas(self, f, area):
        self._deltas = []
        for i in range(self._max_bombs):
            deltas = {}
            for k, (min_value, max_value) in area.items():
                d = i * self._max_radius_ratio * (max_value - min_value) / (self._max_bombs - 1)
                deltas[k] = (-d, d)
            self._deltas.append(deltas)
        return self.generate_new_bombs

    def generate_new_bombs(self, f, area):
        new_bombs = []
        for i, b in enumerate(self._bombs):
            new_bombs += b.explode(f, area, power=self._deltas[i])
        self._bombs = sorted(new_bombs, key=lambda b: b._efficiency)[:self._max_bombs]
        return self.generate_new_bombs
