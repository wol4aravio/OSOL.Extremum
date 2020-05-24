"""Description of Particle Swarm Optimization (PSO) algorithm."""

import random

import numpy as np
from osol.algorithms.template import AlgorithmZeroOrder
from osol.algorithms.tools import bound_vector, generate_point_in_area


class ParticleSwarmOptimization(AlgorithmZeroOrder):
    """PSO implementation."""

    def __init__(self, pop_size, velocity_ratio, c0, c1, c2):
        """Class constructor."""
        self.pop_size = pop_size
        self.velocity_ratio = velocity_ratio
        self.c0 = c0
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
        velocity_area = self.velocity_ratio * velocity_area

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
        v_new = (
            self.c0 * v
            + coefficient_1 * delta_pop_best
            + coefficient_2 * delta_best
        )
        return v_new

    def _iterate(self, f, search_area):
        for i in range(self.pop_size):
            self.velocities[i] = self._update_velocity(
                x=self.pop[i],
                v=self.velocities[i],
                x_pop_best=self.pop_best[i],
                x_best=self.global_best,
            )
            self.pop[i] = bound_vector(
                self.pop[i] + self.velocities[i], search_area,
            )
            self.pop_values[i] = f(self.pop[i])

            if self.pop_values[i] < self.pop_best_values[i]:
                self.pop_best_values[i] = self.pop_values[i]
                self.pop_best[i] = self.pop[i]
                if self.pop_values[i] < self.global_best_value:
                    self.global_best_value = self.pop_values[i]
                    self.global_best = self.pop[i]

    def _terminate(self, f, search_area):
        return self.global_best
