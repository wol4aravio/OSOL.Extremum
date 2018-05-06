import optparse

from OSOL_Extremum.computational_core.computational_core import *


def core_tuner(app, running_port=None, core_path=None):

    parser = optparse.OptionParser()
    parser.add_option("-C", "--core",
                      help="Path to json that describes computational core",
                      type=str)
    parser.add_option("-P", "--port",
                      help="Running port",
                      default=5000)

    if core_path is None:
        options, _ = parser.parse_args()
        path = options.core
    else:
        path = core_path
    if running_port is None:
        try:
            options, _ = parser.parse_args()
            port = options.port
        except Exception:
            port = 5000
    else:
        port = running_port

    app.core = ComputationalCore.from_json(path)
    app.running_port = port
