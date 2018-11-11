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
            self._values = np.array(values)
        else:
            self._values = values
        if keys is None:
            self._keys = [f"_var_{i + 1}" for i in range(len(values))]
        else:
            self._keys = keys

    def __iter__(self):
        """ For `Iterable` """
        return self._values.__iter__()

    def __next__(self):
        """ For `Iterable` """
        return self._values.__next__()

    def keys(self):
        """ Returns list of vector keys """
        return self._keys

    @contract
    def __getitem__(self, item):
        """ Extracts element by key

            :param item: key to extract
            :type item: int|str

            :returns: value that corresponds to the chosen key
            :rtype: number
        """
        if isinstance(item, int):
            return self._values[item]
        elif isinstance(item, str):
            return self._values[self._keys.index(item)]
        else:
            raise KeyError(f"The following key \"{item}\" is not supported")

