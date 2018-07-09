from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


rs_1_config = {
    'RandomSearch': {
        'radius': 1.0
    }
}
rs_2_config = {
    'RandomSearch': {
        'radius': 0.5
    }
}
rs_3_config = {
    'RandomSearch': {
        'radius': 0.1
    }
}

rs_1 = create_algorithm_from_json(rs_1_config)
rs_2 = create_algorithm_from_json(rs_2_config)
rs_3 = create_algorithm_from_json(rs_3_config)


def test_logging():
    log_dir = 'log_test_rs'
    rs_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_random_search():
    logger = logging.getLogger('Random Search')
    assert verifier.verify([rs_1, rs_2, rs_3], logger)
    print('Done!\n')
