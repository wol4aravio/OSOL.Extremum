from abc import ABC, abstractmethod
from contracts import contract, new_contract

from datetime import datetime as dt
from datetime import timedelta


new_contract("function", lambda v_: callable(v_))


class Terminator(ABC):
    """ Abstract class for terminators """

    @contract
    def __init__(self, f):
        """ Initialization of a Terminator

            :param f: target function
            :type f: function
        """
        self._f = f

    @abstractmethod
    @contract(returns=None)
    def reset(self):
        """ Resets Terminator state """
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class MaxCallsTerminator(Terminator):
    """ Terminator that stops execution when maximum allowed number of function calls is exceeded """

    @contract
    def __init__(self, f, max_calls):
        """ Initialization of a MaxCallsTerminator

            :param f: target function
            :type f: function

            :param max_calls: maximum allowed number of function calls
            :type max_calls: int
        """
        super().__init__(f)
        self._max_calls = max_calls
        self._calls = None
        self.reset()

    def reset(self):
        self._calls = 0

    def __call__(self, *args, **kwargs):
        if self._calls >= self._max_calls:
            raise TerminatorExceptions.StopWorkException
        self._calls += 1
        return self._f(*args, **kwargs)


class MaxTimeTerminator(Terminator):
    """ Terminator that stops execution when maximum allowed working time is exceeded """

    @contract
    def __init__(self, f, max_time):
        """ Initialization of a MaxTimeTerminator

            :param f: target function
            :type f: function

            :param max_time: maximum allowed working time
            :type max_time: str
        """
        super().__init__(f)
        self._max_time = max_time
        self._start_time = None

        duration_dict = [s.split(':') for s in max_time.split(',')]
        duration_dict = {k: float(v) for [k, v] in duration_dict}

        self._max_duration = timedelta(days=duration_dict.get('d', 0.0),
                                       hours=duration_dict.get('h', 0.0),
                                       minutes=duration_dict.get('m', 0.0),
                                       seconds=duration_dict.get('s', 0.0))

        self.reset()

    def reset(self):
        self._start_time = dt.now()

    def __call__(self, *args, **kwargs):
        duration = dt.now() - self._start_time
        if duration > self._max_duration:
            raise TerminatorExceptions.StopWorkException
        return self._f(*args, **kwargs)


class TerminatorExceptions:
    """ Class with Termination Exceptions """
    class StopWorkException(Exception):
        """ Exception that is used as a flag to stop current execution """
        pass
