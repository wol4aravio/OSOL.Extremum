from Optimization.Algorithms.RandomSearch import RandomSearch
from Optimization.Algorithms.IntervalExplosionSearch import IntervalExplosionSearch


def create_algorithm_from_json(json_data):
    if 'RandomSearch' in json_data:
        return RandomSearch.from_json(json_data)
    elif 'IntervalExplosionSearch' in json_data:
        return IntervalExplosionSearch.from_json(json_data)
    else:
        raise Exception('Unsupported Optimization Algorithm')
