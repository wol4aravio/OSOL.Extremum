from Optimization.Algorithms.Algorithm import Algorithm
from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator
from Tools.OptimizationTools import create_algorithm_from_json
from Optimization.Algorithms.tools import distance_between_vectors
from Numerical_Objects.Vector import Vector

import numpy as np
import random


class ModifiedHybridMemeticAlgorithm(Algorithm):

    def __init__(self, population_size, distance_bias,
                 pool_size, pool_purge_size,
                 combination_algorithm, combination_terminator,
                 path_relinking_parameter, local_improvement_parameter,
                 delta_path_relinking, delta_local_improvement):
        self._population_size = population_size
        self._distance_bias = distance_bias
        self._pool_size = pool_size
        self._pool_purge_size = pool_purge_size
        self._combination_algorithm = combination_algorithm
        self._combination_terminator = combination_terminator
        self._path_relinking_parameter = path_relinking_parameter
        self._local_improvement_parameter = local_improvement_parameter
        self._delta_path_relinking = delta_path_relinking
        self._delta_local_improvement = delta_local_improvement
        self._iteration_id = None
        self._pool = None

    @classmethod
    def from_dict(cls, dict_data):
        return cls(dict_data['population_size'], dict_data['distance_bias'],
                   dict_data['pool_size'], dict_data['pool_purge_size'],
                   dict_data['combination_algorithm'], dict_data['combination_terminator'],
                   dict_data['path_relinking_parameter'], dict_data['local_improvement_parameter'],
                   dict_data['delta_path_relinking'], dict_data['delta_local_improvement'])

    @classmethod
    def from_json(cls, json_data):
        data = json_data['ModifiedHybridMemeticAlgorithm']
        data['combination_algorithm'] = create_algorithm_from_json(data['combination_algorithm'])
        data['combination_terminator'] = MaxTimeTerminator.from_json(data['combination_terminator'])
        return cls.from_dict(data)

    def to_dict(self):
        return {
            'population_size': self._population_size,
            'distance_bias': self._distance_bias,
            'pool_size': self._pool_size,
            'pool_purge_size': self._pool_purge_size,
            'combination_algorithm': self._combination_algorithm,
            'combination_terminator': self._combination_terminator,
            'path_relinking_parameter': self._path_relinking_parameter,
            'local_improvement_parameter': self._local_improvement_parameter,
            'delta_path_relinking': self._delta_path_relinking,
            'delta_local_improvement': self._delta_local_improvement
        }

    def to_json(self):
        return {'ModifiedHybridMemeticAlgorithm': self.to_dict}

    @property
    def current_state(self):
        if len(self._pool) > 0:
            return {'result': self._pool[0][0], 'efficiency': self._pool[0][1]}
        else:
            return {}

    @property
    def iterations(self):
        return [self.pool_formation,
                self.local_search,
                self.path_relinking,
                self.local_improvement,
                self.pool_renewal]

    def sort_pool(self):
        self._pool = sorted(self._pool, key=lambda kvp: kvp[1])

    def initialize(self, f, area, seed):
        self._iteration_id = 0
        self._pool = []
        if seed is not None:
            if isinstance(seed, list):
                self._pool += sorted(list(map(lambda v: (v, f(v)), seed)), key=lambda kvp: kvp[1])[:self._pool_size]
            else:
                self._pool.append((seed, f(seed)))
        self.sort_pool()

    def pool_formation(self, f, area):

        population = []
        for i in range(self._population_size):
            values = {k: np.random.uniform(*area[k]) for k in area.keys()}
            population.append(Vector(values))
        population = list(map(lambda v: (v, f(v)), population))
        population = sorted(population, key=lambda kvp: kvp[1])
        self._pool.append(population[0])

        if self._iteration_id == 0:
            v_0, val_0 = population[0]
            for v, val in population[1:]:
                if distance_between_vectors(v_0, v) > self._distance_bias:
                    self._pool.append((v, val))
                    break

        self.sort_pool()
        return self.local_search

    @staticmethod
    def get_combination_vector(coefficients, vectors_with_values, area):
        norm = sum(coefficients.values)
        if norm > 0:
            normalized_coefficients = {k: coefficients[k] / norm for k in coefficients.keys}
        else:
            normalized_coefficients = {k: 1.0 / len(area) for k in coefficients.keys}
        combination_vector = Vector({k: 0.0 for k in area.keys()})
        for i, (x, _) in enumerate(vectors_with_values):
            combination_vector += normalized_coefficients['c_{}'.format(i)] * x
        combination_vector = combination_vector.constrain(area)
        return combination_vector

    def local_search(self, f, area):
        while len(self._pool) < self._pool_size:
            pool = self._pool

            def f_combination(coefficients):
                combination_vector = ModifiedHybridMemeticAlgorithm.get_combination_vector(coefficients, pool, area)
                return f(combination_vector)

            combination_area = {'c_{}'.format(i): (0.0, 1.0) for i in range(len(pool))}
            best_combination = self._combination_algorithm.work(f_combination,
                                                                combination_area,
                                                                self._combination_terminator)
            best_vector = ModifiedHybridMemeticAlgorithm.get_combination_vector(best_combination, pool, area)
            f_best_vector = f(best_vector)
            self._pool.append((best_vector, f_best_vector))

        self.sort_pool()
        return self.path_relinking

    def path_relinking(self, f, area):
        delta_pr = self._delta_path_relinking
        for iteration_id in range(self._path_relinking_parameter):
            [p, q, r] = random.sample(range(len(self._pool)), 3)
            x_p = self._pool[p][0]
            x_q = self._pool[q][0]
            x_r = self._pool[r][0]

            x_pq = None
            f_x_pq = np.inf
            for i in range(1, delta_pr):
                x_temp = x_p + (i / delta_pr) * (x_q - x_p)
                f_temp = f(x_temp)
                if f_temp < f_x_pq:
                    x_pq = x_temp
                    f_x_pq = f_temp

            x_new = None
            f_x_new = np.inf
            for i in range(1, delta_pr):
                x_temp = x_pq + (i / delta_pr) * (x_r - x_pq)
                f_temp = f(x_temp)
                if f_temp < f_x_new:
                    x_new = x_temp
                    f_x_new = f_temp

            self._pool.append((x_new, f_x_new))

        self.sort_pool()
        return self.local_improvement

    def local_improvement(self, f, area):
        delta_li = self._delta_local_improvement
        delta_area = {k: delta_li * (max_value - min_value) for k, (min_value, max_value) in area.items()}
        delta_area = {k: (-w, w) for k, w in delta_area.items()}
        for i in range(len(self._pool)):
            for iteration_id in range(self._local_improvement_parameter):
                (x, f_x) = self._pool[i]
                xi = {k: np.random.uniform(*interval) for k, interval in delta_area.items()}
                x_temp = (x >> xi).constrain(area)
                f_x_temp = f(x_temp)
                if f_x_temp < f_x:
                    self._pool[i] = x_temp, f_x_temp

        self.sort_pool()
        return self.pool_renewal

    def pool_renewal(self, f, area):
        self._pool = self._pool[:-self._pool_purge_size]
        to_delete = []
        for i in range(0, len(self._pool)):
            for j in range(i + 1, len(self._pool)):
                if distance_between_vectors(self._pool[i][0], self._pool[j][0]) <= self._distance_bias:
                    to_delete.append(j)

        for i in reversed(sorted(set(to_delete))):
            self._pool.pop(i)
        self._iteration_id += 1
        return self.pool_formation
