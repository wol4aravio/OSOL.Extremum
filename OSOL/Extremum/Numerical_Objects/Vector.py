from OSOL.Extremum.Tools.etc import constrain_point
from OSOL.Extremum.Numerical_Objects.Interval import Interval

import torch
import numpy as np

import random
import math
import json


class Vector:

    def __init__(self, values):
        self._values = values
        self._is_pytorch = False

    def __str__(self):
        return ' x '.join(['({0}: {1})'.format(k, v) for k, v in self._values.items()])

    def __getitem__(self, var_name):
        return self._values[var_name]

    def __setitem__(self, key, value):
        self._values[key] = value

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data)

    @classmethod
    def from_json(cls, json_data):
        values_dict = json_data['Vector']['values']
        for k, v in values_dict.items():
            if isinstance(v, dict):
                if 'Interval' in v:
                    values_dict[k] = Interval.from_dict(v['Interval'])
                else:
                    raise Exception('Can\'t deserialize object: {}'.format(v))
        return cls(values_dict)

    def copy(self):
        return Vector(self._values.copy())

    @property
    def keys(self):
        return set(self._values.keys())

    @property
    def values(self):
        return list(self._values.values())

    @property
    def pytorch_available(self):
        for v in self.values:
            if isinstance(v, Interval):
                return False
        return True

    @property
    def length(self):
        s = 0
        for v in self.values:
            s += v ** 2
        if isinstance(s, Interval):
            return Interval.sqrt(s)
        else:
            return math.sqrt(s)

    @property
    def dim(self):
        return len(self._values)

    def __eq__(self, other):
        if self.keys != other.keys:
            return False
        else:
            for k in (self.keys | other.keys):
                if self[k] != other[k]:
                    return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def to_pytorch_vector(self, dtype=np.float32):
        if self.pytorch_available:
            self._is_pytorch = True
            for k, v in self._values.items():
                self._values[k] = torch.tensor(np.array([v], dtype=dtype), requires_grad=True)
        else:
            raise Exception('Unable to convert to pytorch')

    def to_ordinary_vector(self):
        self._is_pytorch = False
        for k, v in self._values.items():
            self._values[k] = v.tolist()[0]


    def grad(self):
        derivatives = {}
        for k, v in self._values.items():
            derivatives[k] = torch.tensor(self[k].grad)
            self[k].grad.zero_()
        return Vector(derivatives)


    def get_widest_component(self):
        def get_width(v):
            if hasattr(v, 'width'):
                return v.width
            else:
                return 0.0
        max_width = 0.0
        possible_components = []
        for k in self.keys:
            w = get_width(self[k])
            if w == max_width:
                possible_components.append(k)
            else:
                if w > max_width:
                    possible_components = [k]
                    max_width = w
        return random.choice(possible_components)

    def __add__(self, other):
        result = {}
        for k in self.keys | other.keys:
            try:
                result[k] = self[k] + other[k]
            except KeyError:
                raise Exception('Can\'t sum vectors with different keys: {0} VS {1}'.format(self.keys, other.keys))
        return Vector(result)

    def __rshift__(self, delta):
        result = {}
        for k in self.keys:
            result[k] = self[k] + delta.get(k, 0.0)
        return Vector(result)

    def __mul__(self, coefficient):
        result = {}
        for k in self.keys:
            result[k] = coefficient * self[k]
        return Vector(result)

    def __rmul__(self, coefficient):
        return self.__mul__(coefficient)

    def __neg__(self):
        return self * (-1.0)

    def __sub__(self, other):
        return self + other.__neg__()

    def constrain(self, min_max_values):
        result = {}
        for k in self.keys:
            component = self[k]
            target_zone = min_max_values.get(k, (-math.inf, math.inf))
            if hasattr(component, 'constrain'):
                result[k] = component.constrain(*target_zone)
            else:
                result[k] = constrain_point(self[k], *target_zone)
        return Vector(result)

    def split(self, ratios, key=None):
        if key is None:
            split_key = self.get_widest_component()
        else:
            split_key = key

        target_component = self[split_key]
        if hasattr(target_component, 'split'):
            split_result = target_component.split(ratios)
        else:
            split_result = [target_component] * len(ratios)

        final_result = []
        for r in split_result:
            copy = self.copy()
            copy[split_key] = r
            final_result.append(copy)

        return final_result

    def bisect(self, key=None):
        return self.split(ratios=[1.0, 1.0], key=key)

    def reduce_to_dict(self, point_reduction=True):
        result = {}
        for k in self.keys:
            v = self[k]
            if isinstance(v, Interval):
                if point_reduction:
                    result[k] = v.middle_point
                else:
                    result[k] = v
            else:
                result[k] = float(v)
        return result
