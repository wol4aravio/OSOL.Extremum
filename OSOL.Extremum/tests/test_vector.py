from Numerical_Objects.Interval import *
from Numerical_Objects.Vector import *


v1 = Vector({
    'x': 1.0,
    'y': 2.0,
    'z': 3.0
})

v2 = Vector({
    'x': Interval(1.0, 2.0),
    'y': Interval(3.0, 5.0),
    'z': Interval(5.0, 7.0)
})

v3 = Vector({
    'x': 1.0,
    'y': Interval(2.0, 3.0),
    'z': Interval(3.0, 5.0)
})


def test_indexer():
    assert v1['x'] == 1.0
    assert v2['x'] == Interval(1.0, 2.0)


def test_keys():
    assert v1.keys == {'z', 'x', 'y'}
    assert v1.keys == v2.keys


def test_values():
    assert 1 in v1.values
    assert 2 in v1.values
    assert 3 in v1.values
    assert Interval(3.0, 5.0) in v2.values
    assert Interval(2.0, 3.0) in v3.values


def test_equality():
    assert v1 == v1.copy()
    assert v2 == v2.copy()
    assert v3 == v3.copy()


def test_equality():
    assert v1 != v2
    assert v2 != v3
    assert v3 != v1


def test_get_widest_component():
    assert v2.get_widest_component() in ['y', 'z']
    assert v3.get_widest_component() == 'z'
