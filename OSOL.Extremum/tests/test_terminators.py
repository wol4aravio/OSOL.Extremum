from Tools.Encoders import CustomEncoder

from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator

import json


def test_max_time_terminator():
    t = MaxTimeTerminator('m:1,s:30')
    assert t._max_time == MaxTimeTerminator.from_dict({'max_time': t._max_time})._max_time
    assert t._max_time == MaxTimeTerminator.from_json(json.dumps(t, cls=CustomEncoder))._max_time
