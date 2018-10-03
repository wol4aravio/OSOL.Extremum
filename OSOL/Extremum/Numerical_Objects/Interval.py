from OSOL.Extremum.Tools.etc import constrain_point

from configparser import ConfigParser
import warnings
import math


config = ConfigParser()
config.read('OSOL/Extremum/Numerical_Objects/config.ini')


class Interval:
    """This class represents an ordinary interval object [a; b]

    :param lower_bound: lower bound `a`
    :type lower_bound: float

    :param upper_bound: lower bound `b`
    :type upper_bound: float
    
    """

    try:
        __MIN_WIDTH = float(config.get('interval', 'min_width'))
    except Exception:
        warnings.warn('Can not parse config.ini file. Setting default __MIN_WIDTH = 1e-3')
        __MIN_WIDTH = 1e-3

    def __init__(self, lower_bound, upper_bound):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def __str__(self):
        return '[{0}; {1}]'.format(self.left, self.right)

    @classmethod
    def from_value(cls, value):
        return cls(value, value)

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data)

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data['Interval'])

    @staticmethod
    def create_valid_interval(lower_bound, upper_bound):
        if (upper_bound - lower_bound) < Interval.__MIN_WIDTH:
            return 0.5 * (lower_bound + lower_bound)
        else:
            return Interval(lower_bound, upper_bound)
    
    @property
    def left(self):
        return self._lower_bound

    @property
    def right(self):
        return self._upper_bound
    
    @property
    def middle_point(self):
        return 0.5 * (self.left + self.right)

    @property
    def width(self):
        return self.right - self.left

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
        error_left = get_difference(self.left, other.left)
        error_right = get_difference(self.right, other.right)
        return error_left + error_right <= max_error

    def __eq__(self, other):
        if isinstance(other, Interval):
            return self.left == other.left and self.right == other.right
        else:
            return self.left == other and self.right == other

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if isinstance(other, Interval):
            return self.left < other.left
        else:
            return self.left < other

    def __le__(self, other):
        if isinstance(other, Interval):
            return self.left <= other.left
        else:
            return self.left <= other

    def __gt__(self, other):
        if isinstance(other, Interval):
            return self.left > other.left
        else:
            return self.left > other

    def __ge__(self, other):
        if isinstance(other, Interval):
            return self.left >= other.left
        else:
            return self.left >= other

    def __neg__(self):
        return Interval.create_valid_interval(-self.right, -self.left)

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval.create_valid_interval(self.left + other.left, self.right + other.right)
        else:
            return self + Interval.from_value(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval.create_valid_interval(self.left - other.right, self.right - other.left)
        else:
            return self - Interval.from_value(other)

    def __rsub__(self, other):
        return Interval.from_value(other) - self

    def __mul__(self, other):
        if isinstance(other, Interval):
            products = [
                self.left * other.left,
                self.left * other.right,
                self.right * other.left,
                self.right * other.right
            ]
            return Interval.create_valid_interval(min(products), max(products))
        else:
            return self * Interval.from_value(other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Interval):
            if other.left > 0 or other.right < 0:
                return self * Interval.create_valid_interval(1.0 / other.right, 1.0 / other.left)
            elif other.left == 0.0:
                return self * Interval.create_valid_interval(1.0 / other.right, math.inf)
            elif other.right == 0.0:
                return self * Interval.create_valid_interval(-math.inf, 1.0 / other.left)
            else:
                return Interval.create_valid_interval(-math.inf, math.inf)
        else:
            return self / Interval.from_value(other)

    def __rtruediv__(self, other):
        return Interval.from_value(other) / self

    def __pow__(self, power, modulo=None):
        values = [math.pow(self.left, power), math.pow(self.right, power)]
        if power % 2 == 0 and self.left * self.right < 0:
            values.append(0.0)
        values = sorted(values)
        return Interval.create_valid_interval(values[0], values[-1])

    def abs(self):
        values = [math.fabs(self.left), math.fabs(self.right)]
        if self.left * self.right < 0:
            values.append(0.0)
        values = sorted(values)
        return Interval.create_valid_interval(values[0], values[-1])

    def __abs__(self):
        return self.abs()
    
    def _get_trigonometric_points(self):
        c = 0.5 * math.pi
        left_bound = int(math.ceil(self.left / c))
        right_bound = int(math.floor(self.right / c))
        points = [self.left, self.right] + list(map(lambda v: c * v, range(left_bound, right_bound + 1)))
        return points

    def sin(self):
        if self.width > 2.0 * math.pi:
            return Interval(-1.0, 1.0)
        else:
            mapped_points = sorted(map(math.sin, self._get_trigonometric_points()))
            return Interval.create_valid_interval(mapped_points[0], mapped_points[-1])

    def cos(self):
        if self.width > 2.0 * math.pi:
            return Interval(-1.0, 1.0)
        else:
            mapped_points = sorted(map(math.cos, self._get_trigonometric_points()))
            return Interval.create_valid_interval(mapped_points[0], mapped_points[-1])

    def exp(self):
        return Interval.create_valid_interval(math.exp(self.left), math.exp(self.right))

    def sqrt(self):
        if self.right < 0.0:
            raise(Exception('Can\'t perform operation over pure negative interval'))
        else:
            if self.left < 0.0:
                return Interval.create_valid_interval(0.0, math.sqrt(self.right))
            else:
                return Interval.create_valid_interval(math.sqrt(self.left), math.sqrt(self.right))

    def log(self):
        if self.right <= 0.0:
            raise(Exception('Can\'t perform operation over pure negative interval'))
        else:
            if self.left <= 0.0:
                return Interval.create_valid_interval(-math.inf, math.log(self.right))
            else:
                return Interval.create_valid_interval(math.log(self.left), math.log(self.right))

    def constrain(self, min_value, max_value):
        return Interval.create_valid_interval(
            lower_bound=constrain_point(self.left, min_value, max_value),
            upper_bound=constrain_point(self.right, min_value, max_value))

    def split(self, ratios):
        ratio_sum = sum(ratios)
        w = self.width
        intervals = []
        for i in range(len(ratios)):
            intervals.append(
                Interval.create_valid_interval(
                    lower_bound=self.left + sum(ratios[:i]) * w / ratio_sum,
                    upper_bound=self.left + sum(ratios[:(i + 1)]) * w / ratio_sum))
        return intervals

    def bisect(self):
        return self.split(ratios=[1.0, 1.0])


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
