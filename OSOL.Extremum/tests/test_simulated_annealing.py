from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


sa_1_config = {
    'SimulatedAnnealing': {
        'init_temperature': 10.0,
        'C': 0.85,
        'beta': 0.99
    }
}
sa_2_config = {
    'SimulatedAnnealing': {
        'init_temperature': 5.0,
        'C': 0.85,
        'beta': 0.999
    }
}
sa_3_config = {
    'SimulatedAnnealing': {
        'init_temperature': 1.0,
        'C': 0.85,
        'beta': 0.9995
    }
}

sa_1 = create_algorithm_from_json(sa_1_config)
sa_2 = create_algorithm_from_json(sa_2_config)
sa_3 = create_algorithm_from_json(sa_3_config)


def test_logging():
    log_dir = 'log_test_sa'
    sa_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_random_search():
    logger = logging.getLogger('Simulated Annealing')
    assert verifier.verify([sa_1, sa_2, sa_3], logger)
    print('Done!\n')
