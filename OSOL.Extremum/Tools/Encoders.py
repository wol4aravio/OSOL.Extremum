from Numerical_Objects.Interval import Interval

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
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}
