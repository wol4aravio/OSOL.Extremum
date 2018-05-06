from OSOL_Extremum.computational_core.tools import *


def main():
    core_app = create_app()
    core_tuner(core_app)
    core_app.run(port=core_app.running_port)


if __name__ == "__main__":
    main()
