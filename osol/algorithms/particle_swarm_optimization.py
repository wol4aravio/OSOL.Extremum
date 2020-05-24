"""Description of Particle Swarm Optimization (PSO) algorithm."""

import random

import numpy as np
from osol.algorithms.template import AlgorithmZeroOrder
from osol.algorithms.tools import bound_vector, generate_point_in_area


class ParticleSwarmOptimization(AlgorithmZeroOrder):
    """PSO implementation."""

    def __init__(self, pop_size, velocity_ratio, c1, c2):
        """Class constructor."""
        self.pop_size = pop_size
        self.velocity_ratio = velocity_ratio
        self.c1 = c1
        self.c2 = c2

    def _initialize(self, f, search_area):
        self.pop = list()
        self.pop_best = list()
        self.pop_values = list()
        self.pop_best_values = list()
        self.global_best = None
        self.global_best_value = np.inf
        self.velocities = list()

        area_width = search_area[:, 1] - search_area[:, 0]
        velocity_area = np.array([-area_width, area_width]).T
        velocity_area *= 0.5 * self.velocity_ratio

        for _ in range(self.pop_size):
            x = generate_point_in_area(search_area)
            v = generate_point_in_area(velocity_area)
            y = f(x)

            self.pop.append(x)
            self.pop_values.append(y)
            self.velocities.append(v)

            self.pop_best.append(x)
            self.pop_best_values.append(y)

            if y < self.global_best_value:
                self.global_best_value = y
                self.global_best = x

    def _update_velocity(self, x, v, x_pop_best, x_best):
        delta_pop_best = x_pop_best - x
        delta_best = x_best - x
        coefficient_1 = self.c1 * random.uniform(0.0, 1.0)
        coefficient_2 = self.c2 * random.uniform(0.0, 1.0)
        v_new = v + coefficient_1 * delta_pop_best + coefficient_2 * delta_best
        return v_new

    def _iterate(self, f, search_area):
        for pop_id in range(self.pop_size):
            self.velocities[pop_id] = self._update_velocity(
                x=self.pop[pop_id],
                v=self.velocities[pop_id],
                x_pop_best=self.pop_best[pop_id],
                x_best=self.global_best,
            )
            self.pop[pop_id] += self.velocities[pop_id]
            self.pop[pop_id] = bound_vector(self.pop[pop_id], search_area)
            self.pop_values[pop_id] = f(self.pop[pop_id])

            if self.pop_values[pop_id] < self.pop_best_values[pop_id]:
                self.pop_best_values[pop_id] = self.pop_values[pop_id]
                self.pop_best[pop_id] = self.pop[pop_id]
                if self.pop_values[pop_id] < self.global_best_value:
                    self.global_best_value = self.pop_values[pop_id]
                    self.global_best = self.pop[pop_id]

    def _terminate(self, f, search_area):
        return self.global_best
