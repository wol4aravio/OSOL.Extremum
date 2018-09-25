from OSOL.Extremum.Optimization.Algorithms.RandomSearch import RandomSearch
from OSOL.Extremum.Optimization.Algorithms.IntervalExplosionSearch import IntervalExplosionSearch
from OSOL.Extremum.Optimization.Algorithms.AdaptiveRandomSearch import AdaptiveRandomSearch
from OSOL.Extremum.Optimization.Algorithms.SimulatedAnnealing import SimulatedAnnealing
from OSOL.Extremum.Optimization.Algorithms.RandomSearchWithStatisticalAntiGradient import RandomSearchWithStatisticalAntiGradient
from OSOL.Extremum.Optimization.Algorithms.LuusJaakolaOptimization import LuusJaakolaOptimization
from OSOL.Extremum.Optimization.Algorithms.ModifiedHybridRandomSearch import ModifiedHybridRandomSearch
from OSOL.Extremum.Optimization.Algorithms.ModifiedHybridMemeticAlgorithm import ModifiedHybridMemeticAlgorithm
from OSOL.Extremum.Optimization.Algorithms.GradientDescent import GradientDescent


def create_algorithm_from_json(json_data):
    if 'RandomSearch' in json_data:
        return RandomSearch.from_json(json_data)
    elif 'IntervalExplosionSearch' in json_data:
        return IntervalExplosionSearch.from_json(json_data)
    elif 'AdaptiveRandomSearch' in json_data:
        return AdaptiveRandomSearch.from_json(json_data)
    elif 'SimulatedAnnealing' in json_data:
        return SimulatedAnnealing.from_json(json_data)
    elif 'RandomSearchWithStatisticalAntiGradient' in json_data:
        return RandomSearchWithStatisticalAntiGradient.from_json(json_data)
    elif 'LuusJaakolaOptimization' in json_data:
        return LuusJaakolaOptimization.from_json(json_data)
    elif 'ModifiedHybridRandomSearch' in json_data:
        return ModifiedHybridRandomSearch.from_json(json_data)
    elif 'ModifiedHybridMemeticAlgorithm' in json_data:
        return ModifiedHybridMemeticAlgorithm.from_json(json_data)
    elif 'GradientDescent' in json_data:
        return GradientDescent.from_json(json_data)
    else:
        raise Exception('Unsupported Optimization Algorithm')


def parse_additional_ops(key, value):
    if key == 'task_type' or key == 'sampling_type':
        parsed = value
    elif key == 'vars':
        parsed = value.split(',')
    elif key == 'sampling_eps':
        parsed = float(value)
    elif key == 'sampling_max_steps':
        parsed = int(value)
    elif key == 'area' or key == 'control_bounds':
        parsed = []
        for part in value.split(';'):
            [k, min_value, max_value] = part.split(',')
            parsed.append({
                'name': k,
                'min': float(min_value),
                'max': float(max_value)
            })
    elif key == 'initial_conditions':
        parsed = []
        for part in value.split(','):
            [k, k_value] = part.split(',')
            parsed.append({
                'name': k,
                'value': float(k_value)
            })
    else:
        raise Exception('Unsupported key: {}'.format(key))
    return {key: parsed}
