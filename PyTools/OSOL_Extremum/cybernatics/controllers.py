import numpy as np


class PiecewiseConstantController:

    def __init__(self, switch_points, controls):
        self.switch_points = switch_points
        self.controls = controls
        self.timed_control = list(zip(self.switch_points, self.controls))

    def get_control(self, t, x):
        control = [c for (tau, c) in self.timed_control if tau <= t][-1]
        return control


class PiecewiseLinearController:

    def __init__(self, switch_points, controls):
        self.switch_points = switch_points
        self.controls = controls
        time_intervals = list(zip(self.switch_points[:-1], self.switch_points[1:]))
        control_pairs = list(zip(self.controls[:-1], self.controls[1:]))
        self.control_intervals = list(zip(time_intervals, control_pairs))

    def get_control(self, t, x):
        ((t1, t2), (c1, c2)) = next(((t1, t2), c) for ((t1, t2), c) in self.control_intervals if t1 <= t <= t2)
        control = ((t2 - t) * c1 + (t - t1) * c2) / (t2 - t1)
        return control
