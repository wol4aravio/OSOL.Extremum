"""Description of Flower Pollination Algorithm (FPA)."""

import math
import random

import numpy as np
from osol.algorithms.template import AlgorithmZeroOrder
from osol.algorithms.tools import bound_vector, generate_point_in_area


class FlowerPollinationAlgorithm(AlgorithmZeroOrder):
    """FPA implementation."""

    def __init__(self, pop_size, switch_prob, gamma, lambda_value):
        """Class constructor."""
        self.pop_size = pop_size
        self.switch_prob = switch_prob
        self.gamma = gamma
        self.lambda_value = lambda_value

        numerator_1 = math.gamma(1.0 + lambda_value)
        denominator_1 = lambda_value * math.gamma(0.5 * (1 + lambda_value))
        fraction_1 = numerator_1 / denominator_1

        numerator_2 = math.sin(0.5 * math.pi * lambda_value)
        denominator_2 = math.pow(2, 0.5 * (lambda_value - 1))
        fraction_2 = numerator_2 / denominator_2

        self._sigma = math.sqrt(
            math.pow(fraction_1 * fraction_2, 1.0 / lambda_value)
        )

        self.pop = list()
        self.pop_values = list()
        self.best_x = None
        self.best_y = np.inf

    def _initialize(self, f, search_area):
        for _ in range(self.pop_size):
            self.pop.append(generate_point_in_area(search_area))
            self.pop_values.append(f(self.pop[-1]))
            if self.pop_values[-1] < self.best_y:
                self.best_y = self.pop_values[-1]
                self.best_x = self.pop[-1]

    def _Levy(self):
        U = np.random.normal(0, self._sigma)
        V = np.random.normal(0, 1)
        S = U / math.pow(math.fabs(V), 1.0 / self.lambda_value)
        return S

    def _iterate(self, f, search_area):
        for i in range(self.pop_size):
            if random.uniform(0.0, 1.0) < self.switch_prob:
                k = self.gamma * self._Levy()
                self.pop[i] = self.pop[i] + k * (self.best_x - self.pop[i])
            else:
                ids = [j for j in range(self.pop_size) if i != j]
                j, k = random.sample(ids, 2)
                j = int(j)
                k = int(k)
                eps = random.uniform(0.0, 1.0)
                self.pop[i] = self.pop[i] + eps * (self.pop[j] - self.pop[k])
            self.pop[i] = bound_vector(self.pop[i], search_area)
            self.pop_values[i] = f(self.pop[i])
            if self.pop_values[i] < self.best_y:
                self.best_y = self.pop_values[i]
                self.best_x = self.pop[i]

    def _terminate(self, f, search_area):
        return self.best_x
