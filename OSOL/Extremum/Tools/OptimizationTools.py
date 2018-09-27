from OSOL.Extremum.Optimization.Algorithms.RandomSearch import RandomSearch
from OSOL.Extremum.Optimization.Algorithms.IntervalExplosionSearch import IntervalExplosionSearch
from OSOL.Extremum.Optimization.Algorithms.AdaptiveRandomSearch import AdaptiveRandomSearch
from OSOL.Extremum.Optimization.Algorithms.SimulatedAnnealing import SimulatedAnnealing
from OSOL.Extremum.Optimization.Algorithms.RandomSearchWithStatisticalAntiGradient import RandomSearchWithStatisticalAntiGradient
from OSOL.Extremum.Optimization.Algorithms.LuusJaakolaOptimization import LuusJaakolaOptimization
from OSOL.Extremum.Optimization.Algorithms.ModifiedHybridRandomSearch import ModifiedHybridRandomSearch
from OSOL.Extremum.Optimization.Algorithms.ModifiedHybridMemeticAlgorithm import ModifiedHybridMemeticAlgorithm
from OSOL.Extremum.Optimization.Algorithms.DolphinSwarm import DolphinSwarm
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
    elif 'DolphinSwarm' in json_data:
        return DolphinSwarm.from_json(json_data)
    elif 'GradientDescent' in json_data:
        return GradientDescent.from_json(json_data)
    else:
        raise Exception('Unsupported Optimization Algorithm')
