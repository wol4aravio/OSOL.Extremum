from contracts import contract
import numpy as np


class SaturationLimiter:

    @contract
    def __init__(self, min_value=None, max_value=None):
        """ Initialization of SaturationLimiter

            :param min_value: lower available bound
            :type min_value: number|None

            :param max_value: upper available bound
            :type max_value: number|None
        """
        self._min_value = min_value
        self._max_value = max_value

    @contract
    def check(self, v):
        """ Checks input value

            :param v: input value
            :type v: number

            :returns: saturated value
            :rtype: number
        """
        return np.clip(v, a_min=self._min_value, a_max=self._max_value)
