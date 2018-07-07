from Tools.Space import constrain_point
from Numerical_Objects.Interval import Interval

import random
import math
import json


class Vector(dict):

    def __init__(self, values):
        self._values = values
        dict.__init__(self, {'Vector': {'values': self._values}})

    def __getitem__(self, var_name):
        return self._values[var_name]

    def __setitem__(self, key, value):
        self._values[key] = value

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data)

    @classmethod
    def from_json(cls, json_data):
        values_dict = json.loads(json_data)['Vector']['values']
        for k, v in values_dict.items():
            if type(v) == dict:
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

    def __rmul__(self, coefficient):
        result = {}
        for k in self.keys:
            result[k] = coefficient * self[k]
        return Vector(result)

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

        for d in final_result:
            print(d)
            print('\n\n\n')

        return final_result

    def bisect(self, key=None):
        return self.split(ratios=[1.0, 1.0], key=key)

    def reduce_to_solution(self):
        result = {}
        for k in self.keys:
            v = self[k]
            if type(v) == Interval:
                result[k] = v.middle_point
            else:
                result[k] = float(v)
        return result
