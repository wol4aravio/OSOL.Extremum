from Numerical_Objects.Interval import Interval
from Numerical_Objects.Vector import Vector

from Optimization.Tasks.UnconstrainedOptimization import UnconstrainedOptimization
from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator

from Optimization.Algorithms.RandomSearch import RandomSearch
from Optimization.Algorithms.IntervalExplosionSearch import IntervalExplosionSearch
from Optimization.Algorithms.IntervalExplosionSearch import Bomb

import json


class CustomEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Interval):
            return {
                'Interval': {
                    'lower_bound': o.left,
                    'upper_bound': o.right
                }
            }
        elif isinstance(o, Vector):
            return {
                'Vector': {
                    'values': {k: self.default(v) for k, v in o.reduce_to_dict(point_reduction=False).items()}
                }
            }
        elif isinstance(o, UnconstrainedOptimization):
            return {
                'UnconstrainedOptimization': {
                    'f': o._f,
                    'variables': o._variables
                }
            }
        elif isinstance(o, MaxTimeTerminator):
            return {
                'MaxTimeTerminator': {
                    'max_time': o._max_time
                }
            }
        elif isinstance(o, RandomSearch):
            return {
                'RandomSearch': {
                    'radius': o._radius
                }
            }
        elif isinstance(o, IntervalExplosionSearch):
            return {
                'IntervalExplosionSearch': {
                    'max_bombs': o._max_bombs,
                    'max_radius_ratio': o._max_radius_ratio
                }
            }
        elif isinstance(o, Bomb):
            return {
                'Bomb': {
                    'location': self.default(o._location),
                    'efficiency': self.default(o._efficiency)
                }
            }
        return o
