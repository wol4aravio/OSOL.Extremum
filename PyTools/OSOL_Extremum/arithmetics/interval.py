import math


class Interval:

    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @classmethod
    def from_value(cls, value):
        return cls(value, value)

    def __str__(self):
        return '[{0}; {1}]'.format(self.lower_bound, self.upper_bound)

    @property
    def middle_point(self):
        return 0.5 * (self.lower_bound + self.upper_bound)

    @property
    def width(self):
        return self.upper_bound - self.lower_bound

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
        error_left = get_difference(self.lower_bound, other.lower_bound)
        error_right = get_difference(self.upper_bound, other.upper_bound)
        return error_left + error_right <= max_error

    def __neg__(self):
        return Interval(-self.upper_bound, -self.lower_bound)

    def __add__(self, other):
        return Interval(self.lower_bound + other.lower_bound, self.upper_bound + other.upper_bound)

    def __sub__(self, other):
        return Interval(self.lower_bound - other.upper_bound, self.upper_bound - other.lower_bound)

    def __mul__(self, other):
        products = [
            self.lower_bound * other.lower_bound,
            self.lower_bound * other.upper_bound,
            self.upper_bound * other.lower_bound,
            self.upper_bound * other.upper_bound
        ]
        return Interval(min(products), max(products))

    def __truediv__(self, other):
        if other.lower_bound > 0 or other.upper_bound < 0:
            return self * Interval(1.0 / other.upper_bound, 1.0 / other.lower_bound)
        elif other.lower_bound == 0.0:
            return self * Interval(1.0 / other.upper_bound, math.inf)
        elif other.upper_bound == 0.0:
            return self * Interval(-math.inf, 1.0 / other.lower_bound)
        else:
            return Interval(-math.inf, math.inf)

    def pow(self, other):
        if not (other.width == 0.0):
            raise(Exception('[a; b] ^ [c; d] for (d - c) > 0'))
        else:
            power_index = int(other.middle_point)
            values = [math.pow(self.lower_bound, power_index), math.pow(self.upper_bound, power_index)]
            if power_index % 2 == 0 and power_index > 0:
                values.append(0.0)
            values = sorted(values)
            return Interval(values[0], values[-1])

    def abs(self):
        values = [math.fabs(self.lower_bound), math.fabs(self.upper_bound)]
        if self.lower_bound * self.upper_bound < 0:
            values.append(0.0)
        values = sorted(values)
        return Interval(values[0], values[-1])

    def sin(self):
        if self.width > 2.0 * math.pi:
            return Interval(-1.0, 1.0)
        else:
            c = 0.5 * math.pi
            left_bound = int(math.ceil(self.lower_bound / c))
            right_bound = int(math.floor(self.upper_bound / c))
            points = [self.lower_bound, self.upper_bound] + list(map(lambda v: c * v, range(left_bound, right_bound + 1)))
            mapped_points = sorted(map(math.sin, points))
            return Interval(mapped_points[0], mapped_points[-1])

    def cos(self):
        if self.width > 2.0 * math.pi:
            return Interval(-1.0, 1.0)
        else:
            c = 0.5 * math.pi
            left_bound = int(math.ceil(self.lower_bound / c))
            right_bound = int(math.floor(self.upper_bound / c))
            points = [self.lower_bound, self.upper_bound] + list(map(lambda v: c * v, range(left_bound, right_bound + 1)))
            mapped_points = sorted(map(math.cos, points))
            return Interval(mapped_points[0], mapped_points[-1])

    def exp(self):
        return Interval(math.exp(self.lower_bound), math.exp(self.upper_bound))

    def sqrt(self):
        if self.upper_bound < 0.0:
            raise(Exception('Can\'t perform operation to pure negative interval'))
        else:
            if self.lower_bound < 0.0:
                return Interval(0.0, math.sqrt(self.upper_bound))
            else:
                return Interval(math.sqrt(self.lower_bound), math.sqrt(self.upper_bound))

    def log(self):
        if self.upper_bound <= 0.0:
            raise(Exception('Can\'t perform operation to pure negative interval'))
        else:
            if self.lower_bound <= 0.0:
                return Interval(-math.inf, math.log(self.upper_bound))
            else:
                return Interval(math.log(self.lower_bound), math.log(self.upper_bound))


def pow(a, b):
    return a.pow(b)


def abs(i):
    return i.abs()


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
