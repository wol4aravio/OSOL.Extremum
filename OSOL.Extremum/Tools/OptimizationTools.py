from Optimization.Algorithms.RandomSearch import RandomSearch


def create_algorithm_from_json(json_data):
    if 'RandomSearch' in json_data:
        return RandomSearch.from_json(json_data)
    else:
        raise Exception('Unsupported Optimization Algorithm')