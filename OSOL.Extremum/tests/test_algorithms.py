from Optimization.Algorithms.RandomSearch import RandomSearch
from Optimization.Verifier import Verifier


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

rs_1 = RandomSearch.from_json(rs_1_config)
rs_2 = RandomSearch.from_json(rs_2_config)
rs_3 = RandomSearch.from_json(rs_3_config)


def test_random_search():
    logger = logging.getLogger('Random Search')
    assert verifier.verify([rs_1, rs_2, rs_3], logger)
    print('Done!\n')
