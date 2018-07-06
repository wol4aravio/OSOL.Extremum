import random


class Vector(dict):

    def __init__(self, values):
        self._values = values
        dict.__init__(self, {'Vector': self._values})

    def __getitem__(self, var_name):
        return self._values[var_name]

    @property
    def keys(self):
        return set(self._values.keys())

    @property
    def values(self):
        return list(self._values.values())

    def __eq__(self, other):
        for k in self.keys | other.keys:
            try:
                if self[k] != other[k]:
                    return False
            except KeyError:
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
