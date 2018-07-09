import os
import sys
sys.path.append(os.getcwd())

from Tools.OptimizationTools import *
from Tools.Encoders import CustomEncoder

from Optimization.Terminators.MaxTimeTerminator import MaxTimeTerminator

import optparse
import json


def main():

    parser = optparse.OptionParser()
    parser.add_option('-A', '--algorithm',
                      help='Path to algorithm config',
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

    options, _ = parser.parse_args()

    output_file = options.output
    task = create_task_from_json(json.load(open(options.problem, 'r')))
    algorithm = create_algorithm_from_json(json.load(open(options.algorithm, 'r')))
    mt = MaxTimeTerminator(options.time)

    print('Processing')
    x = algorithm.work(task['f'], task['area'], mt)
    json.dump(x, open(output_file, 'w'), cls=CustomEncoder, indent=2)
    print('Done\n')


if __name__ == '__main__':
    main()
