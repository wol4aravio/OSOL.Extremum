from osol.extremum.optimization.algorithms.statistical_anti_gradient_random_search import StatisticalAntiGradientRandomSearch
from osol.extremum.tests.algorithms.verifier import verify


def test():
    sag_rs = StatisticalAntiGradientRandomSearch(radius=0.1, number_of_samples=10)
    assert verify(sag_rs)
