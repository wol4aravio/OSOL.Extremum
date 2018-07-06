from datetime import datetime as dt
from datetime import timedelta


class MaxTimeTerminator(dict):

    def __init__(self, max_time):
        self._max_time = max_time

        duration_dict = dict([s.split(':') for s in max_time.split(',')])
        for k, v in duration_dict.items:
            duration_dict[k] = float(v)
        self._duration = timedelta(days=duration_dict.get('d', 0.0),
                                   hours=duration_dict.get('h', 0.0),
                                   minutes=duration_dict.get('m', 0.0),
                                   seconds=duration_dict.get('s', 0.0))

        dict.__init__(self, {'Terminator': {
            'name': 'MaxTimeTerminator',
            'max_time': self._max_time}})

    def __call__(self, *args, **kwargs):
        current_state = kwargs['current_state']
        if 'start_time' not in current_state:
            current_state['start_time'] = dt.now()
            return False
        else:
            elapsed_time = dt.now() - current_state['start_time']
            if elapsed_time > self._duration:
                return True
            else:
                return False
