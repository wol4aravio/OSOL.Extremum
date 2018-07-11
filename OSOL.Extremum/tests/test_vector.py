from Tools.Encoders import CustomEncoder
from Numerical_Objects.Vector import *

import pytest
import json


v1 = Vector({
    'x': 1.0,
    'y': 2.0,
    'z': 3.0
})

v2 = Vector({
    'y': Interval(3.0, 5.0),
    'z': Interval(5.0, 7.0)
})

v3 = Vector({
    'x': Interval(-1.0, -1.0),
    'y': 3.0,
    'z': Interval(3.0, 5.0)
})


def test_from_dict():
    assert v1 == Vector.from_dict({'values': v1.reduce_to_dict(point_reduction=False)})
    assert v2 == Vector.from_dict({'values': v2.reduce_to_dict(point_reduction=False)})
    assert v3 == Vector.from_dict({'values': v3.reduce_to_dict(point_reduction=False)})


def test_from_json():
    assert v1 == Vector.from_json(json.loads(json.dumps(v1, cls=CustomEncoder)))
    assert v2 == Vector.from_json(json.loads(json.dumps(v2, cls=CustomEncoder)))
    assert v3 == Vector.from_json(json.loads(json.dumps(v3, cls=CustomEncoder)))


def test_indexer():
    assert v1['x'] == 1.0
    assert v2['y'] == Interval(3.0, 5.0)


def test_keys():
    assert v1.keys == {'z', 'x', 'y'}
    assert v1.keys == v3.keys


def test_dim():
    assert v1.dim == 3
    assert v2.dim == 2
    assert v3.dim == 3


def test_values():
    assert 1 in v1.values
    assert 2 in v1.values
    assert 3 in v1.values
    assert Interval(3.0, 5.0) in v2.values
    assert 3 in v3.values


def test_equality():
    assert v1 == v1.copy()
    assert v2 == v2.copy()
    assert v3 == v3.copy()
    assert not v1 == v2


def test_inequality():
    assert v1 != v2
    assert v2 != v3
    assert v3 != v1


def test_get_widest_component():
    assert v2.get_widest_component() in ['y', 'z']
    assert v3.get_widest_component() == 'z'


def test_linear_ops():
    assert v1 + v1 == 2 * v1
    assert v2 + v2 == 2 * v2
    with pytest.raises(Exception):
        v1 + v2
    assert v1 + v3 == Vector({
        'x': 0.0,
        'y': 5.0,
        'z': Interval(6.0, 8.0)
    })


def test_move():
    assert v1 >> {'x': -1.0} == Vector({'x': 0.0, 'y': 2.0, 'z': 3.0})
    assert v3 >> {'x': 1.0, 'z': -3.0} == Vector({'x': 0.0, 'y': 3.0, 'z': Interval(0.0, 2.0)})


def test_constrain():
    assert v1.constrain({'x': (-10, 0)}) == Vector({'x': 0.0, 'y': 2.0, 'z': 3.0})
    assert v3.constrain({'x': (-1.0, 1.0), 'z': (2.0, 4.0)}) == Vector({'x': -1.0, 'y': 3.0, 'z': Interval(3.0, 4.0)})


def test_split():
    results = v3.split([2.0, 2.0, 1.0], key='z')
    assert results[0] == Vector({'x': Interval(-1.0, -1.0), 'y': 3.0, 'z': Interval(3.0, 3.8)})
    assert results[1] == Vector({'x': Interval(-1.0, -1.0), 'y': 3.0, 'z': Interval(3.8, 4.6)})
    assert results[2] == Vector({'x': Interval(-1.0, -1.0), 'y': 3.0, 'z': Interval(4.6, 5.0)})

    results = v3.bisect()
    assert results[0] == Vector({'x': Interval(-1.0, -1.0), 'y': 3.0, 'z': Interval(3.0, 4.0)})
    assert results[1] == Vector({'x': Interval(-1.0, -1.0), 'y': 3.0, 'z': Interval(4.0, 5.0)})

    results = v1.bisect()
    assert results[0] == results[1]


def test_reduce_to_solution():
    assert v3.reduce_to_dict() == {'x': -1.0, 'y': 3.0, 'z': 4.0}
