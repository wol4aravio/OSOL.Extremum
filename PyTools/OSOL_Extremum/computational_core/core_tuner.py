import optparse

from OSOL_Extremum.computational_core.computational_core import *


def core_tuner(app, core_path=None):
    if core_path is None:
        parser = optparse.OptionParser()
        parser.add_option("-C", "--core",
                          help="Path to json that describes computational core",
                          type=str)
        options, _ = parser.parse_args()
        path = options.core
    else:
        path = core_path

    app.core = ComputationalCore.from_json(path)
