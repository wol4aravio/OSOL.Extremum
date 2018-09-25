from OSOL.Extremum.Optimization.Tasks.UnconstrainedOptimization import UnconstrainedOptimization
from OSOL.Extremum.Optimization.Tasks.OpenloopControl import OpenloopControl

from OSOL.Extremum.Cybernetics.DynamicSystem import DynamicSystem

from OSOL.Extremum.Numerical_Objects.Vector import Vector


def create_task_from_json(json_data, pytorch=False):
    result = {}
    if json_data['task_type'] == 'unconstrained_optimization':
        result['f'] = UnconstrainedOptimization(f=json_data['f'], variables=json_data['vars'], pytorch=pytorch)
        result['area'] = {d['name']: (d['min'], d['max']) for d in json_data['area']}
        if 'solution' in json_data:
            result['solution'] = Vector({d['name']: d['value'] for d in json_data['solution']})
    elif json_data['task_type'] == 'openloop_control':
        result['f'] = OpenloopControl(DynamicSystem.from_dict(json_data, pytorch=pytorch))
        result['area'] = {d['name']: (d['min'], d['max']) for d in json_data['area']}
    else:
        raise Exception('Unsupported Task Type')
    return result