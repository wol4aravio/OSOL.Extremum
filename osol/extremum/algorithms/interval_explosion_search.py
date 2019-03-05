from typing import Callable, List, Tuple
from operator import itemgetter

import numpy as np

from osol.extremum.algorithm import Algorithm, check_args
from intervallum.box import Box, BoxVector
from intervallum.box_functions import bisect, constrain
from intervallum.interval import IntervalNumber


class IntervalExplosionSearch(Algorithm):

    def __init__(self, max_radius: List[float]):
        self.bombs_number = None
        self.max_radius = max_radius
        self.bombs = None

    def initialize(self, **kwargs):
        if check_args(["bombs", "f"], **kwargs):
            f = kwargs["f"]
            bombs = kwargs["bombs"]
            self.bombs_number = len(bombs)
            self.bombs = sorted([(b, f(b)) for b in bombs], key=itemgetter(1))

    def terminate(self):
        b = self.bombs[0][0]
        return b.middle if isinstance(b, Box) else b

    def optimize(self, f: Callable[[BoxVector], IntervalNumber],
                 search_area: List[Tuple[float, float]],
                 max_iterations: int):
        iter_id = 0
        explosion_radiuses = [
            np.array(self.max_radius) * (b_id / self.bombs_number)
            for b_id in range(self.bombs_number)]
        while iter_id < max_iterations:
            new_bombs = []
            for b_id, (b, _) in enumerate(self.bombs):
                c_id, pieces = bisect(b)
                part_1, part_2 = pieces[0], pieces[1]

                left = -explosion_radiuses[b_id].copy()
                right = explosion_radiuses[b_id].copy()
                right[c_id] = 0
                part_1 += np.random.uniform(low=left, high=right)
                new_bombs.append(constrain(part_1, search_area))

                right[c_id] = explosion_radiuses[b_id][c_id]
                left[c_id] = 0
                part_2 += np.random.uniform(low=left, high=right)
                new_bombs.append(constrain(part_2, search_area))

            self.bombs = sorted(
                [(b, f(b)) for b in new_bombs],
                key=itemgetter(1))[:self.bombs_number]

        return self.terminate()
