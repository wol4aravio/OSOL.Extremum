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
        self._keys = keys
        self._no_keys = keys is None


v1 = Vector([1, 2.0, 3])
v2 = Vector([1, 2.0, 3], keys=['x', 'y', 'z'])

print(v1._values, v1._keys, v1._no_keys)
print(v2._values, v2._keys, v2._no_keys)
