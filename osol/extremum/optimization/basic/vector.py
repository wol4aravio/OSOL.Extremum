import numpy as np

from contracts import contract, new_contract


new_contract("vector",
             lambda v_: isinstance(v_, Vector))

new_contract("valid_args_tuple",
             lambda v_: all([isinstance(v, int) or isinstance(v, float) for v in v_]))

new_contract("valid_move_tuples",
             lambda v_: all([isinstance(k, (int, str))
                             and isinstance(d, (int, float)) for k, d in v_]))

new_contract("valid_constrain_tuples",
             lambda v_: all([isinstance(k, (int, str)) and
                             isinstance(min_, (int, float)) and
                             isinstance(max_, (int, float)) for k, (min_, max_) in v_]))


class Vector:
    """ Wrapper for more convenient usage of vectors """

    _eq_error = 1e-7

    __slots__ = ['_values', '_keys']

    @contract
    def __init__(self, values, keys=None):
        """ Interval initialization

            :param values: values to be stored
            :type values: list[N](number)|array[N]

            :param keys: indexing keys
            :type keys: NoneType|list[N](str)
        """
        self._values = np.array(values, dtype=np.float32)

        if keys is None:
            self._keys = [f"_var_{i + 1}" for i in range(len(values))]
        else:
            self._keys = keys

    @classmethod
    @contract
    def create(cls, *args, **kwargs):
        """ More general method for Vector creation

            :param args: values without explicitly specified keys
            :type args: valid_args_tuple

            :param kwargs: values with explicitly specified keys
            :type kwargs: dict(str:number)

            :returns: Vector that stores all desired values
            :rtype: vector
        """
        keys = [f"_var_{i + 1}" for i in range(len(args))]
        values = list(args)
        for k, v in kwargs.items():
            keys.append(k)
            values.append(v)
        return cls(values, keys)


    @contract
    def __str__(self):
        """ Prints Vector

            :returns: string representation of a vector
            :rtype: str
        """
        string = [f"{k} -> {self[k]}" for k in self._keys]
        return ", ".join(string)

    def __repr__(self):
        return self.__str__()

    @contract
    def to_tuples(self):
        """ Returns tuples of key-values

            :returns: list of tuples
            :rtype: list(tuple(str, float))
        """
        return [(k, float(v)) for k, v in zip(self._keys, self._values)]

    @contract
    def to_dict(self):
        """ Returns dictionary

            :returns: json dictionary
            :rtype: dict[1](str: dict(str: float))
        """
        return {"Vector": {k: float(v) for k, v in self.to_tuples()}}

    @classmethod
    @contract
    def from_dict(cls, dict_):
        """ Constructs vector from json-dictionary

            :param dict_: dictionary with all parameters
            :type dict_: dict[1](str: dict(str: float))

            :returns: Vector
            :rtype: vector
        """
        keys, values = [], []
        for k, v in dict_["Vector"].items():
            keys.append(k)
            values.append(v)
        return cls(values, keys)

    @contract
    def __len__(self):
        """ Returns number of elements stored in a vector

            :returns: number of elements
            :rtype: int
        """
        return len(self._values)

    def __iter__(self):
        """ For iteration over the elements """
        return self._values.__iter__()

    @contract
    def keys(self):
        """ Returns list of vector keys

            :returns: list of keys
            :rtype: list
        """
        return self._keys.copy()

    @contract
    def __getitem__(self, key):
        """ Extracts element by key

            :param key: key to extract
            :type key: int|str

            :returns: value that corresponds to the chosen key
            :rtype: number
        """
        if isinstance(key, int) and 0 <= key < self.__len__():
            return self._values[key]
        elif isinstance(key, str) and key in self._keys:
            return self._values[self._keys.index(key)]
        else:
            raise KeyError(f"The following key \"{key}\" is not supported")

    def __valid_int_key(self, int_key):
        return isinstance(int_key, int) and 0 <= int_key < self.__len__()

    def __valid_str_key(self, str_key):
        return isinstance(str_key, str) and str_key in self._keys

    @contract
    def __setitem__(self, key, value):
        """ Sets element according to the key

            :param key: chosen key
            :type key: int|str

            :param value: new value to be stored
            :type value: number
        """
        if self.__valid_int_key(key):
            self._values[key] = value
        elif self.__valid_str_key(key):
            self._values[self._keys.index(key)] = value
        else:
            raise KeyError(f"The following key \"{key}\" is not supported")

    def copy(self):
        """ Gets copy of the current vector

            :returns copy of the vector
            :rtype: vector
        """
        return Vector(np.copy(self._values), self.keys())

    def __eq__(self, other):
        """ Equality of vectors

            :param other: second vector
            :type other: vector

            :returns: `True` for equal vectors, `False` - otherwise
            :rtype: bool
        """
        if self._keys == other._keys:
            for i, _ in enumerate(self):
                if np.abs(self[i] - other[i]) > Vector._eq_error:
                    return False
            return True
        else:
            return False

    @contract
    def __mul__(self, coefficient):
        """ Multiplication of a vector by a coefficient

            :param coefficient: multiplier
            :type coefficient: number

            :returns: vector with all values multiplied by coefficient
            :rtype: vector
        """
        return Vector(self._values * coefficient, self._keys)

    @contract
    def __add__(self, other):
        """ Addition of a vector or number to current one

            :param other: vector or number to be added
            :type other: vector|number

            :returns: sum of vector or vector and number
            :rtype: vector
        """
        if isinstance(other, (float, int)):
            return Vector(self._values + other, self._keys)
        else:
            new_values = []
            for i, k in enumerate(self._keys):
                if k in other._keys:
                    new_values.append(self._values[i] + other._values[i])
                else:
                    raise VectorExceptions.DifferentKeysException
            return Vector(new_values, self._keys)

    @contract
    def move(self, *args, **kwargs):
        """ Moves vector according to the arguments

            :param args: list of tuples `<key, moving distance>`
            :type args: valid_move_tuples

            :param kwargs: list of named pairs `<key: moving distance>`
            :type kwargs: dict(str|int: number)|dict[1](str: dict(str: number))

            :returns: moved vector
            :rtype: vector
        """
        if "distance" in kwargs:
            return self.move(**kwargs["distance"])
        moved_vector = self.copy()
        for key, distance in list(args) + list(kwargs.items()):
            if self.__valid_int_key(key):
                moved_vector._values[key] += distance
            elif self.__valid_str_key(key):
                moved_vector._values[self._keys.index(key)] += distance
        return moved_vector

    @contract
    def constrain(self, *args, **kwargs):
        """ Constrains vector according to the arguments

            :param args: list of tuples `<key, (min, max)>`
            :type args: valid_constrain_tuples

            :param kwargs: list of named pairs `<key: (min, max)>`
            :type kwargs: dict(str|int: tuple(number, number))|dict[1](str:dict(str: tuple(number, number)))

            :returns: constrained vector
            :rtype: vector
        """
        if "area" in kwargs:
            return self.constrain(**kwargs["area"])
        constrained_vector = self.copy()
        for key, (min_, max_) in list(args) + list(kwargs.items()):
            if self.__valid_int_key(key):
                constrained_vector._values[key] = np.clip(constrained_vector._values[key], min_, max_)
            elif self.__valid_str_key(key):
                id_ = self._keys.index(key)
                constrained_vector._values[id_] = np.clip(constrained_vector._values[id_], min_, max_)
        return constrained_vector


class VectorExceptions:
    """ New Exceptions for Vector Class """
    class DifferentKeysException(Exception):
        """ Raised when processing vectors need to have the same keys"""
        pass
