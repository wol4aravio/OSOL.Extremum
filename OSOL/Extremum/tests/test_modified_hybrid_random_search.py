from OSOL.Extremum.Tools.OptimizationTools import *
from OSOL.Extremum.Optimization.Verifier import Verifier
from OSOL.Extremum.Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator
from OSOL.Extremum.Optimization.Algorithms.ModifiedHybridRandomSearch import ModifiedHybridRandomSearch

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
rs_w_sag_1_config = {
    'RandomSearchWithStatisticalAntiGradient': {
        'radius': 1.0,
        'number_of_samples': 5
    }
}
rs_w_sag_2_config = {
    'RandomSearchWithStatisticalAntiGradient': {
        'radius': 0.5,
        'number_of_samples': 7
    }
}
rs_w_sag_3_config = {
    'RandomSearchWithStatisticalAntiGradient': {
        'radius': 0.1,
        'number_of_samples': 10
    }
}
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

ars_1 = create_algorithm_from_json(ars_1_config)
ars_2 = create_algorithm_from_json(ars_2_config)
ars_3 = create_algorithm_from_json(ars_3_config)
rs_w_sag_1 = create_algorithm_from_json(rs_w_sag_1_config)
rs_w_sag_2 = create_algorithm_from_json(rs_w_sag_2_config)
rs_w_sag_3 = create_algorithm_from_json(rs_w_sag_3_config)
lj_1 = create_algorithm_from_json(lj_1_config)
lj_2 = create_algorithm_from_json(lj_2_config)
lj_3 = create_algorithm_from_json(lj_3_config)

mt_1 = MaxTimeTerminator.from_json({
    'MaxTimeTerminator': {
        'max_time': 's:5'
    }
})
mt_2 = MaxTimeTerminator.from_json({
    'MaxTimeTerminator': {
        'max_time': 's:3'
    }
})
mt_3 = MaxTimeTerminator.from_json({
    'MaxTimeTerminator': {
        'max_time': 's:1'
    }
})

mhrs_1 = ModifiedHybridRandomSearch(algorithms=[ars_1, rs_w_sag_1, lj_1], terminators=[mt_1, mt_1, mt_1])
mhrs_2 = ModifiedHybridRandomSearch(algorithms=[ars_2, rs_w_sag_2, lj_2], terminators=[mt_2, mt_2, mt_2])
mhrs_3 = ModifiedHybridRandomSearch(algorithms=[ars_3, rs_w_sag_3, lj_3], terminators=[mt_3, mt_3, mt_3])


def test_logging():
    log_dir = 'log_test_mhrs'
    mhrs_1.work(verifier._test_functions[0], verifier._search_area[0], verifier._mt, log_states=log_dir)
    assert len(os.listdir(log_dir)) > 0
    shutil.rmtree(log_dir)


def test_algorithm():
    logger = logging.getLogger('Modified Hybrid Random Search')
    assert verifier.verify([mhrs_1, mhrs_2, mhrs_3], logger)
    print('Done!\n')
