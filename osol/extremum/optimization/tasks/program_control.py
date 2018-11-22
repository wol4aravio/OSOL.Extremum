import fmpy
from fmpy.model_description import read_model_description
from fmpy.util import compile_platform_binary

import os
from contracts import contract


class ProgramControl:
    """ Task: generation of a program control for a FMU defined dynamic system """

    @contract
    def __init__(self, source_dir):
        """ Task initialization

        :param source_dir: directory with exactly one `fmu` and `json` file
        :type source_dir: str
        """
        self._source_dir = source_dir
        self._source_fmu = None
        self._settings_json = None
        files = os.listdir(source_dir)
        for f in files:
            if "fmu" in f:
                if self._source_fmu is None:
                    self._source_fmu = os.path.join(source_dir, f)
                else:
                    raise Exception("Wrong folder contents: several *.fmu files!")
            elif "json":
                if self._settings_json is None:
                    self._settings_json = os.path.join(source_dir, f)
                else:
                    raise Exception("Wrong folder contents: several *.json files!")
        self._platform_compiled_fmu = "_compiled.fmu"
        compile_platform_binary(self._source_fmu, output_filename=self._platform_compiled_fmu)


d = "/Users/wol4aravio/Downloads/spacecraft"
pc = ProgramControl(source_dir=d)
