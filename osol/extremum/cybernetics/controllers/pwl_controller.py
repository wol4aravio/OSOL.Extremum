from contracts import contract

from osol.extremum.cybernetics.controllers.exceptions import ControlGenerationException


class PWLController:

    @contract
    def __init__(self, time_grid, values):
        """ PWL Controller initialization

            :param time_grid: switching points
            :type time_grid: list[N](number)|array[N]

            :param values: corresponding controls
            :type values: list[N](number)|array[N]
        """
        self._time_grid = time_grid
        self._values = values

    @contract
    def generate(self, tau):
        """ Converts input parameter into control

            :param tau: time moment
            :type tau: number

            :returns: control
            :rtype: number
        """
        for i, t0 in enumerate(self._time_grid[:-1]):
            t1 = self._time_grid[i + 1]
            if t0 <= tau <= t1:
                u0, u1 = self._values[i], self._values[i + 1]
                return ((t1 - tau) * u0 + (tau - t0) * u1) / (t1 - t0)
        raise ControlGenerationException(f"Can not generate control for tau <{tau}>")

    def __call__(self, *args, **kwargs):
        return self.generate(kwargs.get("tau", args[0]))
