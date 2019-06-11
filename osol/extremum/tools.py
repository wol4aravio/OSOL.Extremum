from math import inf

from datetime import datetime as dt
from datetime import timedelta


class __WrappedFunction:
    def __init__(self, f, max_evaluations=None, max_time=None):
        self._f = f
        if max_evaluations:
            self._max_evaluations = max_evaluations
        else:
            self._max_evaluations = inf
        if max_time:
            self._max_time = timedelta(seconds=max_time)
        else:
            self._max_time = timedelta(days=365)
        self.reset()

    def __call__(self, *args, **kwargs):
        self._n_evaluations += 1
        return self._f(*args, **kwargs)

    def __repr__(self):
        f_repr = self._f.__repr__()
        remaining_evaluations = self._max_evaluations - self._n_evaluations
        remaining_lifetime = int(self._max_time.total_seconds() - (dt.now() - self._t0).total_seconds())
        remaining_lifetime = max(0, remaining_lifetime)
        return f"WrappedFunction({f_repr}, remaining_evaluations={remaining_evaluations}, remaining_lifetime={remaining_lifetime:.02f} s)"

    def __str__(self):
        return self.__repr__()

    def reset(self):
        self._n_evaluations = 0
        self._t0 = dt.now()

    def check_evaluations(self):
        if not self._max_evaluations:
            return False
        return self._n_evaluations > self._max_evaluations

    def check_time(self):
        if not self._max_time:
            return False
        return dt.now() - self._t0 > self._max_time


def wrap_function(f, max_iterations, max_evaluations, max_time):
    wrapped_function = __WrappedFunction(f, max_evaluations, max_time)
    if max_iterations:
        termination = lambda current_iteration: current_iteration >= max_iterations
    elif max_evaluations:
        termination = lambda current_iteration: wrapped_function.check_evaluations()
    elif max_time:
        termination = lambda current_iteration: wrapped_function.check_time()
    else:
        raise Exception("Termination condition is required")
    return wrapped_function, termination
