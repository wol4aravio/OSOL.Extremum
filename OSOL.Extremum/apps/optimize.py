import os
import sys
sys.path.append(os.getcwd())

from Tools.OptimizationTools import *
from Apps.tools import *
from Tools.Encoders import CustomEncoder
from Numerical_Objects.Vector import Vector

from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator

import optparse
import json


def main():

    parser = optparse.OptionParser()
    parser.add_option('-A', '--algorithm',
                      help='Path to algorithm config',
                      type=str)
    parser.add_option('-S', '--seed',
                      help='Path to seed values',
                      default=None,
                      type=str)
    parser.add_option('-T', '--time',
                      help='Algorithm working time',
                      type=str)
    parser.add_option('-P', '--problem',
                      help='Path to task',
                      type=str)
    parser.add_option('-O', '--output',
                      help='Output file path',
                      type=str)
    parser.add_option('-R', '--reduce',
                      help='Reduce final vector or not',
                      action='store_true',
                      default=False)

    options, _ = parser.parse_args()

    output_file = options.output
    task = create_task_from_json(json.load(open(options.problem, 'r')))
    algorithm = create_algorithm_from_json(json.load(open(options.algorithm, 'r')))
    seed_values = options.seed
    mt = MaxTimeTerminator(options.time)

    print('Processing')
    if seed_values is None:
        x = algorithm.work(task['f'], task['area'], mt)
    else:
        seed_values = [Vector.from_json(json.load(open(f, 'r'))) for f in seed_values.split(',')]
        x = algorithm.work(task['f'], task['area'], mt, seed_values)

    if options.reduce:
        x = Vector(x.reduce_to_dict())
    json.dump(x, open(output_file, 'w'), cls=CustomEncoder, indent=2)
    print('Done\n')


if __name__ == '__main__':
    main()
