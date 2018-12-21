from abc import ABC, abstractmethod
from contracts import contract, ContractsMeta

from datetime import datetime as dt
from datetime import timedelta

from osol.extremum.etc.new_contracts import * # Inclusion of user defined contracts


class Terminator(ABC, metaclass=ContractsMeta):
    """ Abstract class for terminators """

    @contract
    def __init__(self, f, mode):
        """ Initialization of a Terminator

            :param f: target function
            :type f: Function

            :param mode: initialization mode
            :type mode: str
        """
        self._mode = mode
        if mode == "dummy":
            self._f = lambda v: f(v)
        elif mode == "list":
            self._f = lambda v: f(*v)
        elif mode == "dict":
            self._f = lambda v: f(**v)
        else:
            raise TerminatorExceptions.UnsupportedModeException
        self.reset()

    @abstractmethod
    @contract
    def reset(self):
        """ Resets Terminator state

            :rtype: None
        """

    def __call__(self, *args, **kwargs):
        """ Calls the function stored in terminator """
        return self._f(args[0])


class DummyTerminator(Terminator):
    """ Dummy Terminator """

    @contract
    def __init__(self, f, mode):
        """ Initialization of a DummyTerminator

            :param f: target function
            :type f: Function

            :param mode: initialization mode
            :type mode: str
        """
        super().__init__(f, mode)

    def reset(self):
        pass

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class MaxCallsTerminator(Terminator):
    """ Terminator that stops execution when maximum allowed number of function calls is exceeded """

    @contract
    def __init__(self, f, mode, max_calls):
        """ Initialization of a MaxCallsTerminator

            :param f: target function
            :type f: Function

            :param mode: initialization mode
            :type mode: str

            :param max_calls: maximum allowed number of function calls
            :type max_calls: int
        """
        self._calls = None
        self._max_calls = max_calls
        super().__init__(f, mode)

    def reset(self):
        self._calls = 0

    def __call__(self, *args, **kwargs):
        if self._calls >= self._max_calls:
            raise TerminatorExceptions.StopWorkException
        self._calls += 1
        return super().__call__(*args, **kwargs)


class MaxTimeTerminator(Terminator):
    """ Terminator that stops execution when maximum allowed working time is exceeded """

    @contract
    def __init__(self, f, mode, max_time):
        """ Initialization of a MaxTimeTerminator

            :param f: target function
            :type f: Function

            :param mode: initialization mode
            :type mode: str

            :param max_time: maximum allowed working time
            :type max_time: str
        """
        self._max_time = max_time
        self._start_time = None

        duration_dict = [s.split(":") for s in max_time.split(",")]
        duration_dict = {k: float(v) for [k, v] in duration_dict}

        self._max_duration = timedelta(days=duration_dict.get("d", 0.0),
                                       hours=duration_dict.get("h", 0.0),
                                       minutes=duration_dict.get("m", 0.0),
                                       seconds=duration_dict.get("s", 0.0))

        super().__init__(f, mode)

    def reset(self):
        self._start_time = dt.now()

    def __call__(self, *args, **kwargs):
        duration = dt.now() - self._start_time
        if duration > self._max_duration:
            raise TerminatorExceptions.StopWorkException
        return super().__call__(*args, **kwargs)


class TerminatorExceptions:
    """ Class with Termination Exceptions """
    class UnsupportedModeException(Exception):
        """ Exception that is used as a flag for unsupported mode """
        pass

    class StopWorkException(Exception):
        """ Exception that is used as a flag to stop current execution """
        pass
