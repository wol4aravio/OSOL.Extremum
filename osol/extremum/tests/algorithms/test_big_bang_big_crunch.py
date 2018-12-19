from osol.extremum.optimization.algorithms.big_bang_big_crunch import BigBangBigCrunch
from osol.extremum.tests.algorithms.verifier import verify


def test():
    bbbc = BigBangBigCrunch(number_of_points=10, scatter_parameter=1e1, quality_mode="dummy")
    assert verify(bbbc)
