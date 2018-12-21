from osol.extremum.algorithms.random_search import RandomSearch
from osol.extremum.tests.algorithms.verifier import verify


def test():
    rs = RandomSearch(radius=1e-1)
    assert verify(rs)
