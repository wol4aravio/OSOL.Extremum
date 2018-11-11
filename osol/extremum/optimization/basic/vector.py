import numpy as np

from contracts import contract


class Vector:
    """ Wrapper for more convenient usage of vectors """

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
        """
        return Vector(np.copy(self._values), self.keys())
