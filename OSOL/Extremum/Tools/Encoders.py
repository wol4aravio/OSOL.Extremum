import json


def extract_str_type(o):
    return str(type(o))


class CustomEncoder(json.JSONEncoder):

    def default(self, o):
        if extract_str_type(o) == "<class 'OSOL.Extremum.Numerical_Objects.Interval.Interval'>":
            return {
                'Interval': {
                    'lower_bound': o.left,
                    'upper_bound': o.right
                }
            }
        elif extract_str_type(o) == "<class 'OSOL.Extremum.Numerical_Objects.Vector.Vector'>":
            return {
                'Vector': {
                    'values': {k: self.default(v) for k, v in o.reduce_to_dict(point_reduction=False).items()}
                }
            }
        elif extract_str_type(o) == "<class 'OSOL.Extremum.Optimization.Tasks.UnconstrainedOptimization.UnconstrainedOptimization'>":
            return {
                'UnconstrainedOptimization': {
                    'f': o._f,
                    'variables': o._variables
                }
            }
        elif extract_str_type(o) == "<class 'OSOL.Extremum.Optimization.Terminators.MaxTimeTerminator.MaxTimeTerminator'>":
            return {
                'MaxTimeTerminator': {
                    'max_time': o._max_time
                }
            }
        elif extract_str_type(o) == "<class 'OSOL.Extremum.Optimization.Algorithms.RandomSearch.RandomSearch'>":
            return {
                'RandomSearch': {
                    'radius': o._radius
                }
            }
        elif extract_str_type(o) == "<class 'OSOL.Extremum.Optimization.Algorithms.IntervalExplosionSearch.IntervalExplosionSearch'>":
            return {
                'IntervalExplosionSearch': {
                    'max_bombs': o._max_bombs,
                    'max_radius_ratio': o._max_radius_ratio
                }
            }
        elif extract_str_type(o) == "<class 'OSOL.Extremum.Optimization.Algorithms.IntervalExplosionSearch.Bomb'>":
            return {
                'Bomb': {
                    'location': self.default(o._location),
                    'efficiency': self.default(o._efficiency)
                }
            }
        return o
