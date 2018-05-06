import optparse
from flask import Flask, request

from OSOL_Extremum.computational_core.computational_core import *
from OSOL_Extremum.arithmetics.interval import Interval


def create_app():

    app = Flask(__name__)

    @app.route('/process_request', methods=['GET'])
    def process_request():
        args = json.loads(json.dumps(request.args))
        field = args.pop('field')
        scope = args.pop('scope', 'real')
        if scope == 'interval':
            for k in args.keys():
                args[k] = Interval.from_json(args[k])
        elif scope == 'real':
            for k in args.keys():
                args[k] = float(args[k])
        else:
            raise Exception('Unsupported scope: {}'.format(scope))
        return json.dumps(app.core.request(field, args))

    return app


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
