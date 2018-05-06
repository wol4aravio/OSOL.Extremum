import optparse

from OSOL_Extremum.computational_core.tools import *


def main():

    parser = optparse.OptionParser()
    parser.add_option("-C", "--core",
                      help="Path to json that describes computational core",
                      type=str)
    parser.add_option("-P", "--port",
                      help="Running port",
                      default=5000)

    options, _ = parser.parse_args()

    core_app = create_app()

    core_app.core = ComputationalCore.from_json(options.core)
    core_app.run(port=options.port)


if __name__ == "__main__":
    main()
