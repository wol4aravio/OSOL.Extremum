from osol.extremum.algorithms.adaptive_random_search import AdaptiveRandomSearch
from osol.extremum.tests.algorithms.verifier import verify


def test():
    ars = AdaptiveRandomSearch(
        init_radius=2.5,
        factor_small=1.01,
        factor_huge=1.05,
        frequency=5,
        max_no_change=5)
    assert verify(ars)
