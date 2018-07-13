from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


lj_1_config = {
    'LuusJaakolaOptimization': {
        'init_radius': 1.0,
        'number_of_samples': 5,
        'reduction_coefficient': 0.95,
        'recover_coefficient': 0.97,
        'iteration_per_run': 5
    }
}
lj_2_config = {
    'LuusJaakolaOptimization': {
        'init_radius': 0.5,
        'number_of_samples': 7,
        'reduction_coefficient': 0.93,
        'recover_coefficient': 0.98,
        'iteration_per_run': 7
    }
}
lj_3_config = {
    'LuusJaakolaOptimization': {
        'init_radius': 0.1,
        'number_of_samples': 10,
        'reduction_coefficient': 0.9,
        'recover_coefficient': 0.99,
        'iteration_per_run': 10
    }
}

lj_1 = create_algorithm_from_json(lj_1_config)
lj_2 = create_algorithm_from_json(lj_2_config)
lj_3 = create_algorithm_from_json(lj_3_config)


def test_logging():
    log_dir = 'log_test_lj'
    lj_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Luus Jaakola Optimization')
    assert verifier.verify([lj_1, lj_2, lj_3], logger)
    print('Done!\n')
