from OSOL_Extremum.arithmetics.interval import *

i1 = Interval(-1.0, 2.0)
i2 = Interval(-4.0, 3.0)
i3 = Interval(1.0, 2.0)
i4 = Interval(5.0, 5.1)
i5 = Interval(-6.0, -5.0)
i6 = Interval(-2.0, 0.0)
i7 = Interval(0.0, 3.0)


def test_middle_point():
    assert i1.middle_point == 0.5
    assert i3.middle_point == 1.5
    assert i7.middle_point == 1.5


def test_width():
    assert i1.width == 3.0
    assert i3.width == 1.0
    assert i7.width == 3.0


def test_radius():
    assert i1.radius == 1.5
    assert i3.radius == 0.5
    assert i7.radius == 1.5


def test_approximate_equality():
    assert i1.approximately_equals_to(i1 + Interval.from_value(1e-7))
    assert not Interval(-math.inf, 0.0).approximately_equals_to(Interval(-math.inf, math.nan))


def test_addition():
    assert (i1 + i2).approximately_equals_to(Interval(-5.0, 5.0))
    assert (i2 + i3).approximately_equals_to(Interval(-3.0, 5.0))
    assert (i5 + i4).approximately_equals_to(Interval(-1.0, 0.1))


def test_subtraction():
    assert (i1 - i2).approximately_equals_to(Interval(-4.0, 6.0))
    assert (i2 - i3).approximately_equals_to(Interval(-6.0, 2.0))
    assert (i5 - i4).approximately_equals_to(Interval(-11.1, -10.0))


def test_multiplication():
    assert (i1 * i2).approximately_equals_to(Interval(-8.0, 6.0))
    assert (i2 * i3).approximately_equals_to(Interval(-8.0, 6.0))
    assert (i5 * i4).approximately_equals_to(Interval(-30.6, -25.0))


def test_division():
    assert (i1 / i2).approximately_equals_to(Interval(-math.inf, math.inf))
    assert (i2 / i3).approximately_equals_to(Interval(-4.0, 3.0))
    assert (i1 / i5).approximately_equals_to(Interval(-0.4, 0.2))
    assert (i3 / i6).approximately_equals_to(Interval(-math.inf, -0.5))
    assert (i5 / i7).approximately_equals_to(Interval(-math.inf, -5.0/3.0))


def test_power():
    assert (i1 ** 2.0).approximately_equals_to(Interval(0.0, 4.0))
    assert (i2 ** 3.0).approximately_equals_to(Interval(-64.0, 27.0))
    assert (i5 ** 0.0).approximately_equals_to(Interval(1.0, 1.0))


def test_negate():
    assert (-i1).approximately_equals_to(Interval(-2.0, 1.0))
    assert (-i5).approximately_equals_to(Interval(5.0, 6.0))
    assert (-i6).approximately_equals_to(Interval(0.0, 2.0))


def test_sin():
    assert sin(i1).approximately_equals_to(Interval(math.sin(-1.0), 1.0))
    assert sin(i2).approximately_equals_to(Interval(-1.0, 1.0))
    assert sin(i3).approximately_equals_to(Interval(math.sin(1.0), 1.0))
    assert sin(i6).approximately_equals_to(Interval(-1.0, 0.0))


def test_cos():
    assert cos(i1).approximately_equals_to(Interval(math.cos(2.0), 1.0))
    assert cos(i2).approximately_equals_to(Interval(-1.0, 1.0))
    assert cos(i3).approximately_equals_to(Interval(math.cos(2.0), math.cos(1.0)))
    assert cos(i6).approximately_equals_to(Interval(math.cos(-2.0), 1.0))


def test_abs():
    assert abs(i1).approximately_equals_to(Interval(0.0, 2.0))
    assert abs(i2).approximately_equals_to(Interval(0.0, 4.0))
    assert abs(i3).approximately_equals_to(Interval(1.0, 2.0))
    assert abs(i4).approximately_equals_to(Interval(5.0, 5.1))
    assert abs(i5).approximately_equals_to(Interval(5.0, 6.0))
    assert abs(i6).approximately_equals_to(Interval(0.0, 2.0))
    assert abs(i7).approximately_equals_to(Interval(0.0, 3.0))
    

def test_exp():
    assert exp(i1).approximately_equals_to(Interval(math.exp(-1.0), math.exp(2.0)))
    assert exp(i2).approximately_equals_to(Interval(math.exp(-4.0), math.exp(3.0)))
    assert exp(i3).approximately_equals_to(Interval(math.exp(1.0), math.exp(2.0)))


def test_sqrt():
    assert sqrt(i1).approximately_equals_to(Interval(0.0, math.sqrt(2.0)))
    assert sqrt(i3).approximately_equals_to(Interval(math.sqrt(1.0), math.sqrt(2.0)))
    try:
        sqrt(i5)
        bad_op = False
    except Exception:
        bad_op = True
    assert bad_op


def test_log():
    assert log(i1).approximately_equals_to(Interval(-math.inf, math.log(2.0)))
    assert log(i2).approximately_equals_to(Interval(-math.inf, math.log(3.0)))
    assert log(i3).approximately_equals_to(Interval(math.log(1.0), math.log(2.0)))
    assert log(i4).approximately_equals_to(Interval(math.log(5.0), math.log(5.1)))
    try:
        log(i5)
        bad_op = False
    except Exception:
        bad_op = True
    assert bad_op
    try:
        log(i6)
        bad_op = False
    except Exception:
        bad_op = True
    assert bad_op
    assert log(i7).approximately_equals_to(Interval(-math.inf, math.log(3.0)))
