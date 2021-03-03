import numpy as np


def smoke_check(algorithm):
    left, right = -10, 10
    search_area = np.array([[left, right], [left, right]])
    x_opt = np.random.uniform(left, right, 2)
    eps = 1e-2
    x_found = algorithm.optimize(lambda x: np.sum((x - x_opt) ** 2), search_area, 1000)
    return np.linalg.norm(x_found - x_opt) < eps
