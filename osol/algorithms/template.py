"""Template for algorithm development"""

from abc import ABC, abstractmethod

from osol.algorithms.termination import TerminationException
from tqdm import tqdm
from tqdm.notebook import tqdm as tqdm_notebook


class AlgorithmInterface(ABC):
    """General functions that can be applied to any algorithm."""

    def _get_trace_attributes(self, save_trace):
        """Save all non-private attributes."""
        if not save_trace:
            return
        if not hasattr(self, "trace"):
            setattr(self, "trace", list())
        names = [a for a in dir(self) if not a.startswith("_")]
        names = [
            a
            for a in names
            if a
            not in ("trace", "initialize", "iterate", "terminate", "optimize")
        ]
        values = {n: getattr(self, n) for n in names}
        setattr(self, "trace", getattr(self, "trace") + [values])

    def _log_attrs(self, verbose_attrs):
        if verbose_attrs:
            for attribute in verbose_attrs:
                print(
                    "{name}: {value}".format(
                        name=attribute, value=getattr(self, attribute),
                    )
                )


class AlgorithmZeroOrder(AlgorithmInterface):
    """Basic class for all optimization algorithms."""

    @abstractmethod
    def _initialize(self, f, search_area):
        """Initialization step."""

    @abstractmethod
    def _iterate(self, f, search_area):
        """Iterative step."""

    @abstractmethod
    def _terminate(self, f, search_area):
        """Termination step"""

    def initialize(self, f, search_area, save_trace, verbose_attrs):
        """Initialization step."""
        self._initialize(f, search_area)
        self._get_trace_attributes(save_trace)
        self._log_attrs(verbose_attrs)

    def iterate(self, f, search_area, save_trace, verbose_attrs):
        """Iterative step."""
        self._iterate(f, search_area)
        self._get_trace_attributes(save_trace)
        self._log_attrs(verbose_attrs)

    def terminate(self, f, search_area, save_trace, verbose_attrs):
        """Termination step"""
        solution = self._terminate(f, search_area)
        self._get_trace_attributes(save_trace)
        self._log_attrs(verbose_attrs)
        return solution

    def optimize(self, f, search_area, number_of_iterations, **kwargs):
        """Optimization procedure."""
        save_trace = kwargs.get("save_trace", False)
        verbose_attrs = kwargs.get("verbose_attrs", None)
        self.initialize(f, search_area, save_trace, verbose_attrs)
        iteration_range = range(number_of_iterations)
        if "progress_bar" in kwargs:
            if kwargs["progress_bar"] == "jupyter":
                iteration_range = tqdm_notebook(iteration_range)
            elif kwargs["progress_bar"] == "console":
                iteration_range = tqdm(iteration_range)
            else:
                print("{} is not supported".format(kwargs["progress_bar"]))
        for _ in iteration_range:
            try:
                self.iterate(f, search_area, save_trace, verbose_attrs)
            except TerminationException:
                break
        solution = self.terminate(f, search_area, save_trace, verbose_attrs)
        return solution


class AlgorithmFirstOrder(AlgorithmInterface):
    """Basic class for all optimization algorithms."""

    @abstractmethod
    def _initialize(self, f, g, search_area):
        """Initialization step."""

    @abstractmethod
    def _iterate(self, f, g, search_area):
        """Iterative step."""

    @abstractmethod
    def _terminate(self, f, g, search_area):
        """Termination step"""

    def initialize(self, f, g, search_area, save_trace, verbose_attrs):
        """Initialization step."""
        self._initialize(f, g, search_area)
        self._get_trace_attributes(save_trace)
        self._log_attrs(verbose_attrs)

    def iterate(self, f, g, search_area, save_trace, verbose_attrs):
        """Iterative step."""
        self._iterate(f, g, search_area)
        self._get_trace_attributes(save_trace)
        self._log_attrs(verbose_attrs)

    def terminate(self, f, g, search_area, save_trace, verbose_attrs):
        """Termination step"""
        solution = self._terminate(f, g, search_area)
        self._get_trace_attributes(save_trace)
        self._log_attrs(verbose_attrs)
        return solution

    def optimize(self, f, g, search_area, num_of_iterations, **kwargs):
        """Optimization procedure."""
        save_trace = kwargs.get("save_trace", False)
        verbose_attrs = kwargs.get("verbose_attrs", None)
        self.initialize(f, g, search_area, save_trace, verbose_attrs)
        for _ in range(num_of_iterations):
            try:
                self.iterate(f, g, search_area, save_trace, verbose_attrs)
            except TerminationException:
                break
        solution = self.terminate(f, g, search_area, save_trace, verbose_attrs)
        return solution
