from OSOL.Extremum.Tools.OptimizationTools import *
from OSOL.Extremum.Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


gd_1_config = {
    'GradientDescent': {
        'alpha': 1e-1
    }
}
gd_2_config = {
    'GradientDescent': {
        'alpha': 1e-2
    }
}
gd_3_config = {
    'GradientDescent': {
        'alpha': 1e-3
    }
}

gd_1 = create_algorithm_from_json(gd_1_config)
gd_2 = create_algorithm_from_json(gd_2_config)
gd_3 = create_algorithm_from_json(gd_3_config)


def test_logging():
    log_dir = 'log_test_gd'
    gd_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Gradient Descent')
    assert verifier.verify([gd_1, gd_2, gd_3], logger)
    print('Done!\n')
