import os
import json
from contracts import contract
import tempfile

import numpy as np

from fmpy import extract
from fmpy.model_description import read_model_description
from fmpy.util import compile_platform_binary
from fmpy.fmi2 import printLogMessage
from fmpy.fmi2 import fmi2CallbackFunctions, fmi2CallbackLoggerTYPE, fmi2CallbackAllocateMemoryTYPE, fmi2CallbackFreeMemoryTYPE
from fmpy.fmi2 import FMU2Slave
from fmpy.fmi2 import allocateMemory, freeMemory
from fmpy.simulation import Input, Recorder, apply_start_values


class FMUModel:
    """ Interface for a FMU model """

    @contract
    def __init__(self, model, description, needs_compilation):
        """ Model initialization

        :param model: model `fmu` file
        :type model: str

        :param description: model description in a `json`
        :type description: str

        :param needs_compilation: flag for compilation
        :type needs_compilation: bool
        """
        self._model = model
        self._description = description
        self._needs_compilation = needs_compilation

        if needs_compilation:
            self._compiled_model = "_" + next(tempfile._get_candidate_names()) + ".fmu"
            FMUModel.compile_fmu(model, self._compiled_model)
        else:
            self._compiled_model = model

        with open(description, "r") as d:
            self._settings = json.load(d)

        model_description = read_model_description(self._compiled_model, validate=True)
        if model_description.coSimulation is None:
            raise Exception("Unsupported model type")
        self._model_description = model_description

        if os.path.isfile(os.path.join(self._compiled_model, "modelDescription.xml")):
            unzipdir = self._compiled_model
        else:
            tempdir = extract(self._compiled_model)
            unzipdir = tempdir

        fmu_args = {"guid": model_description.guid,
                    "unzipDirectory": unzipdir,
                    "instanceName": None,
                    "fmiCallLogger": None, 
                    "modelIdentifier": model_description.coSimulation.modelIdentifier}
        self._fmu_args = fmu_args

        logger = printLogMessage
        callbacks = fmi2CallbackFunctions()
        callbacks.logger = fmi2CallbackLoggerTYPE(logger)
        callbacks.allocateMemory = fmi2CallbackAllocateMemoryTYPE(allocateMemory)
        callbacks.freeMemory = fmi2CallbackFreeMemoryTYPE(freeMemory)
        self._callbacks = callbacks

    @staticmethod
    @contract
    def compile_fmu(file, output_file):
        """ FMU sources compilation

            :param file: input model name
            :type file: str

            :param output_file: output model name
            :type output_file: str

            :rtype: None
        """
        compile_platform_binary(file, output_filename=output_file)

    @contract
    def _purge(self):
        """ Removes compiled fmu

            :rtype: None
        """
        if self._needs_compilation:
            os.remove(self._compiled_model)

    def __enter__(self):
        """ For context manager support

            :returns: ref to itself
        """
        return self

    @contract
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ For context manager support

            :rtype: None
        """
        self._purge()

    @contract
    def simulate(self, initial_state, termination_time, dt, controllers):
        """ Simulates behaviour of the model

            :param initial_state: inital values of the model
            :type initial_state: dict(str:number)

            :param termination_time: maximum operating time
            :type termination_time: number,>0

            :param dt: time delta
            :type dt: number,>0

            :param controllers: information about the controllers
            :type controllers: dict(str:dict(str:*))

            :returns: list of trajectories
            :rtype: tuple(dict(str:array), dict(str:array))
        """
        fmu = FMU2Slave(**self._fmu_args)
        fmu.instantiate(callbacks=self._callbacks, loggingOn=False)

        model_description = self._model_description
        start_time = 0.0

        fmu.setupExperiment(tolerance=model_description.defaultExperiment.tolerance, startTime=start_time)

        input_ = Input(fmu=fmu, modelDescription=model_description, signals=None)
        time = start_time

        initial_values = {self._settings["aliases"].get(k, k): v for k, v in initial_state.items()}
        apply_start_values(fmu, model_description, initial_values, apply_default_start_values=False)
        input_.apply(time)

        vars_ref = {}
        for variable in model_description.modelVariables:
            vars_ref[variable.name] = variable.valueReference
        vars_ref["t"] = vars_ref["internalTime"]

        fmu.enterInitializationMode()
        fmu.exitInitializationMode()

        recorder = Recorder(
            fmu=fmu,
            modelDescription=model_description,
            variableNames=self._settings["state_variables"],
            interval=dt)

        control_history = {control_name: [] for control_name in controllers.keys()}
        while time < termination_time:
            recorder.sample(time, force=True)
            input_.apply(time)
            controls = dict()
            for control_name, control_params in controllers.items():
                u = control_params["f"]
                input_vars = fmu.getReal([vars_ref[n] for n in control_params["inputs"]])
                controls[vars_ref[control_name]] = u(*input_vars)
                control_history[control_name].append(controls[vars_ref[control_name]])
            fmu.setReal(*zip(*list(controls.items())))
            fmu.doStep(currentCommunicationPoint=time, communicationStepSize=dt)
            time += dt

        recorder.sample(time, force=True)

        fmu.terminate()
        fmu.freeInstance()
        recorded = recorder.result()
        states = dict()
        for i, n in enumerate(["t"] + self._settings["state_variables"]):
            states[n] = np.array([r[i] for r in recorded])
        for control_name, control_values in control_history.items():
            control_history[control_name] = np.array(control_values)
        return states, control_history
