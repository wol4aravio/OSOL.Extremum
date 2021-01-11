"""Flower Pollination Algorithm."""

from typing import overload

import numpy as np
from scipy.special import gamma as gamma_function

from osol.extremum.algorithms.algorithm import Algorithm
from osol.extremum.algorithms.tools import bound_vector, generate_point_in_area


class FPA(Algorithm):
    """FPA description."""

    def __init__(self, N, p, gamma, lambda_):
        """Initialization procedure.

        N - number of flowers
        p - switch probability
        gamma - scaling factor
        lambda_ - Levy distribution parameter
        """
        super().__init__()
        self.N = N
        self.p = p
        self.gamma = gamma
        self.lambda_ = lambda_

    @overload
    def initialize(self, f, search_area):
        """Initialization step."""
        self.flowers_locations = [
            generate_point_in_area(search_area) for _ in range(self.N)
        ]
        self.flowers_values = [f(x) for x in self.flowers_locations]
        self.id_best_flower = np.argmin(self.flowers_values)

    @staticmethod
    def _levy_flight(lambda_):
        fraction_1 = gamma_function(1 + lambda_) / (
            lambda_ * gamma_function(0.5 * (1 + lambda_))
        )
        fraction_2 = np.sin(0.5 * np.pi * lambda_) / (
            2.0 ** (0.5 * (lambda_ - 1))
        )
        sigma_squared = (fraction_1 * fraction_2) ** (1.0 / lambda_)
        U = np.random.normal(scale=sigma_squared)
        V = np.random.normal()
        return U / (np.abs(V) ** (1 / lambda_))

    @staticmethod
    def _levy_flight_multidim(lambda_, dims):
        return np.array([FPA._levy_flight(lambda_) for _ in range(dims)])

    def _global_pollination(self, flower):
        return flower + self.gamma * FPA._levy_flight_multidim(
            self.lambda_, len(self.flower)
        ) * (self.flowers_locations[self.id_best_flower] - flower)

    def _local_pollination(self, flower):
        [id_1, id_2] = np.random.choice(range(self.N), size=2, replace=False)
        return flower + np.random.uniform() * (
            self.flowers_locations[id_1] - self.flowers_locations[id_2]
        )

    def iterate(self, f, search_area):
        """Iterative step."""
        for flower_id in range(self.N):
            flower = self.flowers_locations[flower_id]
            flower_value = self.flowers_values[flower_id]
            if np.random.uniform() < self.p:
                new_flower = self._global_pollination(flower)
            else:
                new_flower = self._local_pollination(flower)
            new_flower = bound_vector(new_flower, search_area)
            new_flower_value = f(new_flower)
            if new_flower_value < flower_value:
                self.flowers_locations[flower_id] = new_flower
                self.flowers_values[flower_id] = new_flower_value
        self.id_best_flower = np.argmin(self.flowers_values)

    def terminate(self, _, __):
        """Termination step"""
        return self.flowers_locations(self.id_best_flower)
