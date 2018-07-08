from Optimization.Terminators.Terminator import Terminator

from datetime import datetime as dt
from datetime import timedelta

import json


class MaxTimeTerminator(Terminator):

    def __init__(self, max_time):
        self._max_time = max_time
        self.start_time = None

        duration_dict = dict([s.split(':') for s in max_time.split(',')])
        for k, v in duration_dict.items():
            duration_dict[k] = float(v)
        self._duration = timedelta(days=duration_dict.get('d', 0.0),
                                   hours=duration_dict.get('h', 0.0),
                                   minutes=duration_dict.get('m', 0.0),
                                   seconds=duration_dict.get('s', 0.0))

        dict.__init__(self, {'Terminator': {
            'name': 'MaxTimeTerminator',
            'max_time': self._max_time}})

    @classmethod
    def from_dict(cls, dict_data):
        return cls(max_time=dict_data['Terminator']['max_time'])

    @classmethod
    def from_json(cls, json_data):
        return MaxTimeTerminator.from_dict(json.loads(json_data))

    def initialize(self):
        self.start_time = dt.now()

    def __call__(self, *args, **kwargs):
        elapsed_time = dt.now() - self.start_time
        if elapsed_time > self._duration:
            return True
        else:
            return False
