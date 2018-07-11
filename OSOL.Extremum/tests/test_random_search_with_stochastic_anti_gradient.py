from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


rs_w_sag1_config = {
    'RandomSearchWithStatisticalAntiGradient': {
        'radius': 1.0,
        'number_of_samples': 5
    }
}
rs_w_sag2_config = {
    'RandomSearchWithStatisticalAntiGradient': {
        'radius': 0.5,
        'number_of_samples': 7
    }
}
rs_w_sag3_config = {
    'RandomSearchWithStatisticalAntiGradient': {
        'radius': 0.1,
        'number_of_samples': 10
    }
}

rs_w_sag1 = create_algorithm_from_json(rs_w_sag1_config)
rs_w_sag2 = create_algorithm_from_json(rs_w_sag2_config)
rs_w_sag3 = create_algorithm_from_json(rs_w_sag3_config)


def test_logging():
    log_dir = 'log_test_rs_w_sag'
    rs_w_sag1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_random_search():
    logger = logging.getLogger('Random Search With Statistical Anti Gradient')
    assert verifier.verify([rs_w_sag1, rs_w_sag2, rs_w_sag3], logger)
    print('Done!\n')
