from contracts import contract

import numpy as np

from osol.extremum.cybernetics.controllers.exceptions import ControlGenerationException


class PWCController:

    @contract
    def __init__(self, time_grid, values):
        """ PWC Controller initialization

            :param time_grid: switching points
            :type time_grid: list[N](number)|array[N]

            :param values: corresponding controls
            :type values: list[N](number)|array[N]
        """
        self._time_grid = time_grid
        if isinstance(time_grid, list):
            self._time_grid.append(np.inf)
        else:
            self._time_grid = np.append(self._time_grid, np.inf)
        self._values = values

    @contract
    def generate(self, tau):
        """ Converts input parameter into control

            :param tau: time moment
            :type tau: number

            :returns: control
            :rtype: number
        """
        for i, t in enumerate(self._time_grid[:-1]):
            if t <= tau < self._time_grid[i + 1]:
                return self._values[i]
        raise ControlGenerationException(f"Can not generate control for tau <{tau}>")

    def __call__(self, *args, **kwargs):
        return self.generate(kwargs.get("tau", args[0]))
