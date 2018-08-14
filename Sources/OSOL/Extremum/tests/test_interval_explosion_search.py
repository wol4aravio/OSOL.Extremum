from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier

import os
import shutil
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


def test_logging():
    log_dir = 'log_test_ies'
    ies_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Interval Explosion Search')
    assert verifier.verify([ies_1, ies_2, ies_3], logger)
    print('Done!\n')
