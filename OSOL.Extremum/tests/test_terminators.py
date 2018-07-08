from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator

import json


def test_max_time_terminator():
    t = MaxTimeTerminator('m:1,s:30')
    assert t == MaxTimeTerminator.from_dict(dict(t))
    assert t == MaxTimeTerminator.from_json(json.dumps(t))
