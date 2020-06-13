"""Description of Explosion Search (ES) algorithm."""

import operator
import random
from collections import namedtuple

import numpy as np
from osol.algorithms.template import AlgorithmZeroOrder
from osol.algorithms.tools import bound_vector, generate_point_in_area

BOMB = namedtuple("Bomb", ["location", "value"])


class ExplosionSearch(AlgorithmZeroOrder):
    """ES implementation."""

    def __init__(self, b_max, power_max):
        """Class constructor."""
        self.b_max = b_max
        self.power_max = power_max
        self._bombs_power_vectors = [
            coefficient * power_max
            for coefficient in np.linspace(0, 1, num=b_max)
        ]

    def _initialize(self, f, search_area):
        bombs = list()
        for _ in range(self.b_max):
            x = generate_point_in_area(search_area)
            y = f(x)
            bombs.append(BOMB(x, y))
        self.bombs = sorted(bombs, key=operator.attrgetter("value"))
        self.best_bomb = self.bombs[0]

    def _iterate(self, f, search_area):
        bombs = list()
        for bomb, radius in zip(self.bombs, self._bombs_power_vectors):
            n_dim = search_area.shape[0]
            split_direction = random.randint(0, n_dim - 1)
            explosion_area = radius * np.concatenate(
                (-np.ones(n_dim), np.ones(n_dim))
            )
            explosion_area = explosion_area.reshape(-1, 2, order="F")
            # print("==========")
            # print(self._bombs_power_vectors)
            # print("==========")

            explosion_area[split_direction, 1] = 0.0
            new_bomb = bomb.location + generate_point_in_area(explosion_area)
            new_bomb = bound_vector(new_bomb, search_area)
            bombs.append(BOMB(new_bomb, f(new_bomb)))

            explosion_area[split_direction, :] = -explosion_area[
                split_direction, :
            ]
            new_bomb = bomb.location + generate_point_in_area(explosion_area)
            new_bomb = bound_vector(new_bomb, search_area)
            bombs.append(BOMB(new_bomb, f(new_bomb)))

        self.bombs = sorted(bombs, key=operator.attrgetter("value"))
        self.bombs = self.bombs[: self.b_max]
        self.best_bomb = self.bombs[0]

    def _terminate(self, f, search_area):
        return self.best_bomb.location
