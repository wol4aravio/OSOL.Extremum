"""Various tools for demo apps."""

import numpy as np
import plotly.graph_objects as go


class DemoFunction:
    """Demo function class - used in streamlit apps."""

    def __init__(self, f, name):
        self.f = f
        self.name = name

    def __call__(self, x):
        return self.f(x)


DEMO_FUNC_1 = DemoFunction(
    lambda x: (x ** 2).sum(), "Sum of Squares: x ^ 2 + y ^ 2",
)
DEMO_FUNC_2 = DemoFunction(
    lambda x: np.abs(x).sum(), "Sum of Absolute Values: |x| + |y|",
)
DEMO_FUNC_3 = DemoFunction(
    lambda x: (x[0] - x[1]) ** 2, "Squared Difference: (x - y) ^ 2",
)

DEMO_FUNCTIONS = [DEMO_FUNC_1, DEMO_FUNC_2, DEMO_FUNC_3]
SEARCH_AREA = np.array([[-10, 10], [-10, 10]])

###############################################################################


def generate_contours(f, area):
    """Make contour plot for given function."""
    x = np.linspace(area[0, 0], area[0, 1], 101)
    y = np.linspace(area[1, 0], area[1, 1], 101)
    z = np.zeros(shape=(len(x), len(y)))
    for i, _x in enumerate(x):
        for j, _y in enumerate(y):
            z[i, j] = f(np.array([_x, _y]))
    return go.Contour(z=z, x=x, y=y)
