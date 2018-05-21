from functools import partial
import json

from OSOL_Extremum.computational_core.unconstrained_optimization import *
from OSOL_Extremum.computational_core.openloop_control import *


class ComputationalCore:

    def __init__(self, operations):
        self.operations = operations

    def request(self, op_name, op_args):
        return self.operations[op_name](op_args)

    @classmethod
    def from_json(cls, json_file):
        with open(json_file) as json_data:
            task_info = json.load(json_data)
            if task_info['task_type'] == 'unconstrained_optimization':
                task = UnconstrainedOptimization.from_dict(task_info)
                operations = {'f': task.f}
                if hasattr(task, '_df'):
                    for k in task._df.keys():
                        operations['df_{}'.format(k)] = partial(task.df, k)
            elif task_info['task_type'] == 'openloop_control':
                task = OpenloopControl.from_dict(task_info)
                operations = {
                    'sim': task.sim,
                    'sim_out': task.outer_sim
                }
            else:
                raise Exception('Unsupported task type')
            return cls(operations)

