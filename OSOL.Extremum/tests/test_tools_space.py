from Tools.Space import *


def test_constrain():
    assert constrain_point(x=0.0, min_value=-10.0, max_value=10.0) == 0.0
    assert constrain_point(x=-12.0, min_value=-10.0, max_value=10.0) == -10.0
    assert constrain_point(x=33.0, min_value=-10.0, max_value=10.0) == 10.0
