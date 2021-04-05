import numpy as np


class FeldbaumTestFunctions:
    @staticmethod
    def _generate_function(a, b, c, p):
        return lambda x: np.sum(a * np.abs(x - c) ** p) + b

    def __init__(self, N, dim, random=True, a=None, b=None, c=None, p=None):
        self._N = N
        self._dim = dim
        if random:
            self._a = np.random.uniform(low=0.0, high=5.0, size=(N, dim))
            self._b = np.random.uniform(low=-10.0, high=10.0, size=(N, 1))
            self._c = np.random.uniform(low=-10.0, high=10.0, size=(N, dim))
            self._p = np.random.uniform(low=0.0, high=2.5, size=(N, dim))
        else:
            self._a = a
            self._b = b
            self._c = c
            self._p = p
        self._functions = [
            FeldbaumTestFunctions._generate_function(
                self._a[i, :], self._b[i, :], self._c[i, :], self._p[i, :]
            )
            for i in range(N)
        ]

    def __call__(self, x):
        return np.min([f(x) for f in self._functions])
