from OSOL.Extremum.Tools.OptimizationTools import *
from OSOL.Extremum.Optimization.Verifier import Verifier

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()


ds_1_config = {
    'DolphinSwarm': {
        'number_of_dolphins': 10,
        'speed': 1.0,
        'search_time': 5,
        'number_of_directions': 5,
        'acceleration': 1,
        'maximum_transmission_time': 10,
        'radius_reduction_coefficient': 2.1
    }
}
ds_2_config = {
    'DolphinSwarm': {
        'number_of_dolphins': 5,
        'speed': 0.1,
        'search_time': 5,
        'number_of_directions': 10,
        'acceleration': 1,
        'maximum_transmission_time': 10,
        'radius_reduction_coefficient': 2.5
    }
}
ds_3_config = {
    'DolphinSwarm': {
        'number_of_dolphins': 10,
        'speed': 0.01,
        'search_time': 10,
        'number_of_directions': 3,
        'acceleration': 1,
        'maximum_transmission_time': 10,
        'radius_reduction_coefficient': 3.0
    }
}

ds_1 = create_algorithm_from_json(ds_1_config)
ds_2 = create_algorithm_from_json(ds_2_config)
ds_3 = create_algorithm_from_json(ds_3_config)


def test_logging():
    log_dir = 'log_test_ds'
    ds_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Dolphin Swarm')
    assert verifier.verify([ds_1, ds_2, ds_3], logger)
    print('Done!\n')
