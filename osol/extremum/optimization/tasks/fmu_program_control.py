import fmpy
from fmpy.model_description import read_model_description
from fmpy.util import compile_platform_binary

import os
import json
from contracts import contract

import numpy as np


class FMUProgramControl:
    """ Task: generation of a program control for a FMU defined dynamic system """

    @contract
    def __init__(self, source_dir):
        """ Task initialization

        :param source_dir: directory with exactly one `fmu` and `json` file
        :type source_dir: str
        """
        self._source_dir = source_dir
        self._source_fmu = None
        self._settings = None
        files = os.listdir(source_dir)
        for f in files:
            if "fmu" in f:
                if self._source_fmu is None:
                    self._source_fmu = os.path.join(source_dir, f)
                else:
                    raise Exception("Wrong folder contents: several *.fmu files!")
            elif "json":
                if self._settings is None:
                    with open(os.path.join(source_dir, f), 'r') as j:
                        self._settings = json.load(j)
                else:
                    raise Exception("Wrong folder contents: several *.json files!")
        self._platform_compiled_fmu = "_compiled.fmu"
        compile_platform_binary(self._source_fmu, output_filename=self._platform_compiled_fmu)
        self._model_description = read_model_description(self._platform_compiled_fmu)

        self._output_connectors = {"_t": 0}
        for settings_output_name in [settings["var_name"] for settings in self._settings["criteria"]]:
            for i, fmu_output_name in enumerate(self._model_description.outputs):
                if settings_output_name in str(fmu_output_name):
                    self._output_connectors[settings_output_name] = i + 1

    @contract
    def simulate(self, initial_state, parameters=None, t0=None, t1=None, step=None):
        """ Simulates model for the given state and parameters

        :param initial_state: initial state values
        :type initial_state: dict(str:number)

        :param parameters: additional model parameters
        :type parameters: dict(str:number)|None

        :param t0: initial time
        :type t0: None|number

        :param t1: termination time
        :type t1: None|number

        :param step: step size
        :type step: None|number

        :returns: dict with state values
        :rtype: dict(str:array)
        """
        if parameters is None:
            parameters = dict()

        tunable_values = {}
        for k, v in (list(initial_state.items()) + list(parameters.items())):
            tunable_values[self.alias.get(k, k)] = v

        result = fmpy.simulate_fmu(
            self._platform_compiled_fmu,
            start_time=(t0 or self.t0),
            stop_time=(t1 or self.t1),
            output_interval=(step or self.step),
            start_values=tunable_values)

        return {k: np.array([r[i] for r in result]) for k, i in self._output_connectors.items()}

    @staticmethod
    @contract
    def _process_integral_criterion(sim_result, criterion_settings):
        """ Processes `integral` type of criterion

        :param sim_result: simulation results
        :type sim_result: dict(str:array)

        :param criterion_settings: criterion settings
        :type criterion_settings: dict(str:str|number)

        :returns: criterion value
        :rtype: number
        """
        var_name = criterion_settings["var_name"]
        weight = criterion_settings["weight"]
        return weight * sim_result[var_name][-1]

    @staticmethod
    @contract
    def _process_terminal_criterion(sim_result, criterion_settings):
        """ Processes `terminal` type of criterion

        :param sim_result: simulation results
        :type sim_result: dict(str:array)

        :param criterion_settings: criterion settings
        :type criterion_settings: dict(str:str|number)

        :returns: criterion value
        :rtype: number
        """
        var_name = criterion_settings["var_name"]
        weight = criterion_settings["weight"]
        target = criterion_settings["target"]
        tolerance = criterion_settings["tolerance"]
        metric_type = criterion_settings["metric_type"]

        error = np.abs(sim_result[var_name][-1] - target)
        if error <= tolerance:
            return error
        return weight * np.power(error, int(metric_type[1:]))

    @contract
    def get_criterion_value(self, sim_results):
        """ Extracts unified criterion value from simulation results

        :param sim_results: simulation results
        :type sim_results: dict(str:array)

        :returns: criterion value
        :rtype: dict(str:number)
        """
        criterion_values = dict()

        for criterion_settings in self.criteria:
            name = criterion_settings["name"]
            criterion_type = criterion_settings["type"]

            if criterion_type == "integral":
                criterion_values[name] = FMUProgramControl._process_integral_criterion(sim_results, criterion_settings)
            elif criterion_type == "terminal":
                criterion_values[name] = FMUProgramControl._process_terminal_criterion(sim_results, criterion_settings)
            else:
                raise Exception(f"Unsupported criterion type: {criterion_type} for {name}")

        return criterion_values

    @contract
    def purge(self):
        """ Removes created files

        :rtype: None
        """
        os.remove(self._platform_compiled_fmu)

    @property
    @contract(returns="number")
    def t0(self):
        """ Start time """
        return self._settings["time"]["start"]

    @property
    @contract(returns="number")
    def t1(self):
        """ Termination time """
        return self._settings["time"]["end"]

    @property
    @contract(returns="number")
    def step(self):
        """ Step size """
        return self._settings["time"]["step"]

    @property
    @contract(returns="dict(str:str)")
    def alias(self):
        """ Step size """
        return self._settings["alias"]

    @property
    @contract(returns="list(dict(str:*))")
    def criteria(self):
        """ Criterion Settings """
        return self._settings["criteria"]
