from Tools.Space import constrain_point

from configparser import ConfigParser

import math
import json

config = ConfigParser()
config.read('Numerical_Objects/config.ini')


class Interval(dict):

    __MIN_WIDTH = float(config.get('interval', 'min_width'))

    def __init__(self, lower_bound, upper_bound):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        dict.__init__(self, {'Interval': {
            'lower_bound': self._lower_bound,
            'upper_bound': self._upper_bound}})

    def __str__(self):
        return '[{0}; {1}]'.format(self.l, self.u)

    @classmethod
    def from_value(cls, value):
        return cls(value, value)

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data['Interval'])

    @classmethod
    def from_json(cls, json_data):
        return cls(**json.loads(json_data)['Interval'])

    @staticmethod
    def create_valid_interval(lower_bound, upper_bound):
        if (upper_bound - lower_bound) < Interval.__MIN_WIDTH:
            return 0.5 * (lower_bound + lower_bound)
        else:
            return Interval(lower_bound, upper_bound)
        
    @property
    def l(self):
        return self._lower_bound

    @property
    def u(self):
        return self._upper_bound
    
    @property
    def middle_point(self):
        return 0.5 * (self.l + self.u)

    @property
    def width(self):
        return self.u - self.l

    @property
    def radius(self):
        return self.width / 2.0

    def approximately_equals_to(self, other, max_error=1e-5):
        def get_difference(a, b):
            delta = math.fabs(a - b)
            if math.isnan(delta):
                if a == b:
                    return 0.0
                else:
                    return 1.0
            else:
                return delta
        error_left = get_difference(self.l, other.l)
        error_right = get_difference(self.u, other.u)
        return error_left + error_right <= max_error

    def __eq__(self, other):
        if type(other) == Interval:
            return self.l == other.l and self.u == other.u
        else:
            return self.l == other and self.u == other

    def __ne__(self, other):
        return not (self == other)

    def __neg__(self):
        return Interval.create_valid_interval(-self.u, -self.l)

    def __add__(self, other):
        if type(other) == Interval:
            return Interval.create_valid_interval(self.l + other.l, self.u + other.u)
        else:
            return self + Interval.from_value(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if type(other) == Interval:
            return Interval.create_valid_interval(self.l - other.u, self.u - other.l)
        else:
            return self - Interval.from_value(other)

    def __rsub__(self, other):
        return Interval.from_value(other) - self

    def __mul__(self, other):
        if type(other) == Interval:
            products = [
                self.l * other.l,
                self.l * other.u,
                self.u * other.l,
                self.u * other.u
            ]
            return Interval.create_valid_interval(min(products), max(products))
        else:
            return self * Interval.from_value(other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) == Interval:
            if other.l > 0 or other.u < 0:
                return self * Interval.create_valid_interval(1.0 / other.u, 1.0 / other.l)
            elif other.l == 0.0:
                return self * Interval.create_valid_interval(1.0 / other.u, math.inf)
            elif other.u == 0.0:
                return self * Interval.create_valid_interval(-math.inf, 1.0 / other.l)
            else:
                return Interval.create_valid_interval(-math.inf, math.inf)
        else:
            return self / Interval.from_value(other)

    def __rtruediv__(self, other):
        return Interval.from_value(other) / self

    def __pow__(self, power, modulo=None):
        values = [math.pow(self.l, power), math.pow(self.u, power)]
        if power % 2 == 0 and self.l * self.u < 0:
            values.append(0.0)
        values = sorted(values)
        return Interval.create_valid_interval(values[0], values[-1])

    def abs(self):
        values = [math.fabs(self.l), math.fabs(self.u)]
        if self.l * self.u < 0:
            values.append(0.0)
        values = sorted(values)
        return Interval.create_valid_interval(values[0], values[-1])

    def __abs__(self):
        return self.abs()

    def sin(self):
        if self.width > 2.0 * math.pi:
            return Interval(-1.0, 1.0)
        else:
            c = 0.5 * math.pi
            left_bound = int(math.ceil(self.l / c))
            right_bound = int(math.floor(self.u / c))
            points = [self.l, self.u] + list(map(lambda v: c * v, range(left_bound, right_bound + 1)))
            mapped_points = sorted(map(math.sin, points))
            return Interval.create_valid_interval(mapped_points[0], mapped_points[-1])

    def cos(self):
        if self.width > 2.0 * math.pi:
            return Interval(-1.0, 1.0)
        else:
            c = 0.5 * math.pi
            left_bound = int(math.ceil(self.l / c))
            right_bound = int(math.floor(self.u / c))
            points = [self.l, self.u] + list(map(lambda v: c * v, range(left_bound, right_bound + 1)))
            mapped_points = sorted(map(math.cos, points))
            return Interval.create_valid_interval(mapped_points[0], mapped_points[-1])

    def exp(self):
        return Interval.create_valid_interval(math.exp(self.l), math.exp(self.u))

    def sqrt(self):
        if self.u < 0.0:
            raise(Exception('Can\'t perform operation to pure negative interval'))
        else:
            if self.l < 0.0:
                return Interval.create_valid_interval(0.0, math.sqrt(self.u))
            else:
                return Interval.create_valid_interval(math.sqrt(self.l), math.sqrt(self.u))

    def log(self):
        if self.u <= 0.0:
            raise(Exception('Can\'t perform operation to pure negative interval'))
        else:
            if self.l <= 0.0:
                return Interval.create_valid_interval(-math.inf, math.log(self.u))
            else:
                return Interval.create_valid_interval(math.log(self.l), math.log(self.u))

    def constrain(self, min_value, max_value):
        return Interval.create_valid_interval(constrain_point(self.l, min_value, max_value),
                                              constrain_point(self.u, min_value, max_value))

    def split(self, ratios):
        ratio_sum = sum(ratios)
        w = self.width
        intervals = []
        for i in range(len(ratios)):
            intervals.append(Interval(self.l + sum(ratios[:i]) * w / ratio_sum, self.l + sum(ratios[:(i+1)]) * w / ratio_sum))
        return intervals

    def bisect(self):
        return self.split([1.0, 1.0])


def sin(i):
    return i.sin()


def cos(i):
    return i.cos()


def exp(i):
    return i.exp()


def sqrt(i):
    return i.sqrt()


def log(i):
    return i.log()
