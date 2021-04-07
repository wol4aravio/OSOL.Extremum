import numpy as np

from osol.algorithms.abstract import OptimizationAlgorithm
from osol.tools.vectors import bound_vector, generate_vector_in_area


class BlackHoleOptimization(OptimizationAlgorithm):
    def __init__(self, N):
        self.N = N

    def _calculate_quality_levels(self, f):
        self.values = [f(x) for x in self.stars]
        min_value = np.min(self.values)
        self.quality_levels = [1 + v - min_value for v in self.values]

    def _black_hole_update(self):
        self.black_hole_id = int(np.argmin(self.quality_levels))

    def _move_stars(self, f, search_area):
        black_hole = self.stars[self.black_hole_id]
        self.stars = [
            s + np.random.rand() * (black_hole - s)
            for i, s in enumerate(self.stars)
            if i != self.black_hole_id
        ]
        self.stars = [bound_vector(s, search_area) for s in self.stars] + [black_hole]
        self._calculate_quality_levels(f)

    def _check_event_horizon(self, f, search_area):
        black_hole = self.stars[self.black_hole_id]
        black_hole_level = self.quality_levels[self.black_hole_id]
        radius = black_hole_level / (np.sum(self.quality_levels) - black_hole_level)
        for i, star in enumerate(self.stars):
            if i == self.black_hole_id:
                continue
            if np.linalg.norm(black_hole - star) < radius:
                self.stars[i] = generate_vector_in_area(search_area)
        self._calculate_quality_levels(f)

    def initialize(self, f, search_area):
        self.stars = [generate_vector_in_area(search_area) for _ in range(self.N)]
        self._calculate_quality_levels(f)

    def iterate(self, f, search_area):
        self._black_hole_update()
        self._move_stars(f, search_area)
        self._black_hole_update()
        self._check_event_horizon(f, search_area)

    def terminate(self, _, __):
        return self.stars[self.black_hole_id]
