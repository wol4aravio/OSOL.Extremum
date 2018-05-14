import numpy as np


class PiecewiseConstantController:

    def __init__(self, switch_points, controls):
        self.switch_points = switch_points
        self.controls = controls
        self.timed_control = list(zip(self.switch_points, self.controls))

    def get_control(self, t, x):
        control = [c for (tau, c) in self.timed_control if tau <= t][-1]
        return control












