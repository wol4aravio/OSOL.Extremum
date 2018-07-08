from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier


import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


ies_1_config = {
    'IntervalExplosionSearch': {
        'max_bombs': 10,
        'max_radius_ratio': 0.1
    }
}

ies_2_config = {
    'IntervalExplosionSearch': {
        'max_bombs': 25,
        'max_radius_ratio': 0.25
    }
}

ies_3_config = {
    'IntervalExplosionSearch': {
        'max_bombs': 10,
        'max_radius_ratio': 0.01
    }
}

ies_1 = create_algorithm_from_json(ies_1_config)
ies_2 = create_algorithm_from_json(ies_2_config)
ies_3 = create_algorithm_from_json(ies_3_config)


def test_interval_explosion_search():
    logger = logging.getLogger('Interval Explosion Search')
    assert verifier.verify([ies_1, ies_2, ies_3], logger)
    print('Done!\n')
