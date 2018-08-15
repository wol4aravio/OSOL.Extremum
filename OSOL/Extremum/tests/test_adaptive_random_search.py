from OSOL.Extremum.Tools.OptimizationTools import *
from OSOL.Extremum.Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


ars_1_config = {
    'AdaptiveRandomSearch': {
        'init_radius': 1.0,
        'factor_small': 1.1,
        'factor_huge': 1.5,
        'frequency': 5,
        'max_no_change': 5
    }
}
ars_2_config = {
    'AdaptiveRandomSearch': {
        'init_radius': 1.0,
        'factor_small': 1.05,
        'factor_huge': 1.25,
        'frequency': 5,
        'max_no_change': 5
    }
}
ars_3_config = {
    'AdaptiveRandomSearch': {
        'init_radius': 1.0,
        'factor_small': 1.01,
        'factor_huge': 1.1,
        'frequency': 5,
        'max_no_change': 5
    }
}

ars_1 = create_algorithm_from_json(ars_1_config)
ars_2 = create_algorithm_from_json(ars_2_config)
ars_3 = create_algorithm_from_json(ars_3_config)


def test_logging():
    log_dir = 'log_test_ars'
    ars_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Adaptive Random Search')
    assert verifier.verify([ars_1, ars_2, ars_3], logger)
    print('Done!\n')
