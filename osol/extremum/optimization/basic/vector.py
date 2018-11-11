import numpy as np

from contracts import contract, new_contract


new_contract("Vector", lambda v_: isinstance(v_, Vector))


class Vector:
    """ Wrapper for more convenient usage of vectors """

    _eq_error = 1e-7

    @contract
    def __init__(self, values, keys=None):
        """ Interval initialization

            :param values: values to be stored
            :type values: list[N](number)|array[N]

            :param keys: indexing keys
            :type keys: NoneType|list[N](str)
        """
        if isinstance(values, np.ndarray):
            self._values = values
        else:
            self._values = np.array(values)
        if keys is None:
            self._keys = [f"_var_{i + 1}" for i in range(len(values))]
        else:
            self._keys = keys

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
    def to_dict(self):
        """ Returns dictionary

            :returns: json dictionary
            :rtype: dict[1](str: dict(str: float))
        """
        return {"Vector": {k: float(v) for k, v in zip(self._keys, self._values)}}

    @classmethod
    @contract
    def from_dict(cls, dict_):
        """ Constructs vector from json-dictionary

            :param dict_: dictionary with all parameters
            :type dict_: dict[1](str: dict(str: float))

            :returns: Vector
            :rtype: Vector
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

    @contract
    def __setitem__(self, key, value):
        """ Sets element according to the key

            :param key: chosen key
            :type key: int|str

            :param value: new value to be stored
            :type value: number
        """
        if isinstance(key, int) and 0 <= key < self.__len__():
            self._values[key] = value
        elif isinstance(key, str) and key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            raise KeyError(f"The following key \"{key}\" is not supported")

    def copy(self):
        """ Gets copy of the current vector

            :returns copy of the vector
            :rtype: Vector
        """
        return Vector(np.copy(self._values), self.keys())

    def __eq__(self, other):
        """ Equality of vectors

            :param other: second vector
            :type other: Vector

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
            :rtype: Vector
        """
        return Vector(self._values * coefficient, self._keys)

    @contract
    def __add__(self, other):
        """ Addition of a vector or number to current one

            :param other: vector or number to be added
            :type other: Vector|number

            :returns: sum of vector or vector and number
            :rtype: Vector
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


class VectorExceptions:

    class DifferentKeysException(Exception):
        pass
