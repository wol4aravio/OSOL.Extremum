from OSOL_Extremum.cybernatics.dynamic_system import DynamicSystem


class OpenloopControl:

    def __init__(self, ds):
        self.ds = ds

    def sim(self, parameters):
        times, states, controls, I_integral, I_terminal, error_terminal_state, phase_errors = self.ds.simulate(parameters)
        return I_integral + I_terminal + error_terminal_state + sum(phase_errors)

    @classmethod
    def from_dict(cls, data):
        return cls(DynamicSystem.from_dict(data))