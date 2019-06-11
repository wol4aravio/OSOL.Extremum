import numpy as np

from osol.extremum.tools import wrap_function

def _create_rotation_matrix(n, i, j, theta):
    R = np.eye(n)
    R[i, i] = R[j, j] = np.cos(theta)
    R[i, j] = R[j, i] = np.sin(theta)
    R[i, j] *= -1
    return R


def _create_composition_rotation_matrix(n, theta):
    R = np.eye(n)
    for i in range(1, n):
        for j in range(1, i + 1):
            _i = n - i
            _j = n + 1 - j
            R = np.dot(R, _create_rotation_matrix(n, _i - 1, _j - 1, theta))
    return R


def _make_step(x0, r, theta, x_origin=None):
    n = len(x0)
    R = _create_composition_rotation_matrix(n, theta)
    S = r * R

    if x_origin is None:
        x_origin = np.zeros_like(x0)

    return np.dot(S, x0) - np.dot(S - np.eye(n), x_origin)


def spiral_optimization(f, area, m, r, theta, max_iterations=None, max_evaluations=None, max_time=None):
    min_ = area[:, 0].reshape(-1, 1)
    max_ = area[:, 1].reshape(-1, 1)

    wrapped_function, termination = wrap_function(f, max_iterations, max_evaluations, max_time)
    points = np.random.uniform(min_, max_, size=(area.shape[0], m))
    point_values = np.apply_along_axis(lambda x: wrapped_function(x), axis=0, arr=points)
    x_origin = points[:, np.argmin(point_values)]

    current_iteration = 0
    while not termination(current_iteration):
        for i in range(m):
            points[:, i] = _make_step(points[:, i], r, theta, x_origin)
        points = np.clip(points, min_, max_)
        point_values = np.apply_along_axis(lambda x: wrapped_function(x), axis=0, arr=points)
        x_origin = points[:, np.argmin(point_values)]
        current_iteration += 1
    return x_origin, f(x_origin)
