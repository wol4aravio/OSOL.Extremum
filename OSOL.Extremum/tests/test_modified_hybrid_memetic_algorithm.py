from Tools.OptimizationTools import *
from Optimization.Verifier import Verifier
from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator

import os
import shutil
import logging
logging.basicConfig(level=logging.INFO)


verifier = Verifier()

rs_config = {
    'RandomSearch': {
        'radius': 0.1
    }
}
rs = create_algorithm_from_json(rs_config)
mt = MaxTimeTerminator.from_json({
    'MaxTimeTerminator': {
        'max_time': 's:0.1'
    }
})

mhma_1_config = {
    'ModifiedHybridMemeticAlgorithm': {
        'population_size': 10,
        'distance_bias': 0.1,
        'pool_size': 5,
        'pool_purge_size': 5,
        'combination_algorithm': rs,
        'combination_terminator': mt,
        'path_relinking_parameter': 5,
        'local_improvement_parameter': 5,
        'delta_path_relinking': 5,
        'delta_local_improvement': 0.01
    }
}
mhma_2_config = {
    'ModifiedHybridMemeticAlgorithm': {
        'population_size': 25,
        'distance_bias': 0.01,
        'pool_size': 3,
        'pool_purge_size': 2,
        'combination_algorithm': rs,
        'combination_terminator': mt,
        'path_relinking_parameter': 3,
        'local_improvement_parameter': 3,
        'delta_path_relinking': 3,
        'delta_local_improvement': 0.01
    }
}
mhma_3_config = {
    'ModifiedHybridMemeticAlgorithm': {
        'population_size': 5,
        'distance_bias': 0.1,
        'pool_size': 3,
        'pool_purge_size': 1,
        'combination_algorithm': rs,
        'combination_terminator': mt,
        'path_relinking_parameter': 10,
        'local_improvement_parameter': 10,
        'delta_path_relinking': 10,
        'delta_local_improvement': 0.05
    }
}

mhma_1 = create_algorithm_from_json(mhma_1_config)
mhma_2 = create_algorithm_from_json(mhma_2_config)
mhma_3 = create_algorithm_from_json(mhma_3_config)


def test_logging():
    log_dir = 'log_test_mhma'
    mhma_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Modified Hybrid Memetic Algorithm')
    assert verifier.verify([mhma_1, mhma_2, mhma_3], logger)
    print('Done!\n')
