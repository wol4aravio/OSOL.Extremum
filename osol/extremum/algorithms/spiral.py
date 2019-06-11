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


def _make_step(x0, r, theta, x_origin):
    n = len(x0)
    S = r * _create_composition_rotation_matrix(n, theta)
    return np.dot(S, x0) - np.dot(S - np.eye(n), x_origin)


def _initialize(area, m, max_, min_):
    return np.random.uniform(min_, max_, size=(area.shape[0], m))


def _get_current_best(points, wrapped_function):
    point_values = np.apply_along_axis(lambda x: wrapped_function(x), axis=0, arr=points)
    x_best = points[:, np.argmin(point_values)]
    return x_best


def spiral_optimization(f, area, max_iterations=None, max_evaluations=None, max_time=None, m=25, r=0.95, theta=(np.pi / 4)):
    min_ = area[:, 0].reshape(-1, 1)
    max_ = area[:, 1].reshape(-1, 1)

    wrapped_function, termination = wrap_function(f, max_iterations, max_evaluations, max_time)
    stepper = lambda x: _make_step(x, r, theta, x_best)

    points = _initialize(area, m, max_, min_)
    x_best = _get_current_best(points, wrapped_function)

    current_iteration = 0
    while not termination(current_iteration):
        points = np.apply_along_axis(stepper, axis=0, arr=points)
        points = np.clip(points, min_, max_)
        x_best = _get_current_best(points, wrapped_function)
        current_iteration += 1
    return x_best
