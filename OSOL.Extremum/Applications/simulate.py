import os
import sys
sys.path.append(os.getcwd())

from Cybernatics.DynamicSystem import DynamicSystem
from Optimization.Tasks.OpenloopControl import OpenloopControl

import optparse
import json


def main():

    parser = optparse.OptionParser()
    parser.add_option('-D', '--dynamic_system',
                      help='Path to dynamic system',
                      type=str)
    parser.add_option('-C', '--control',
                      help='Path to control',
                      type=str)
    parser.add_option('-O', '--output',
                      help='Output file path',
                      type=str)
    parser.add_option('-R', '--reduce',
                      help='Reduce final vector or not',
                      action='store_true',
                      default=False)

    options, _ = parser.parse_args()

    print('Processing')
    ds = DynamicSystem.from_dict(json.load(open(options.dynamic_system, 'r')))
    task = OpenloopControl(ds)
    task.outer_sim(options.control, options.output, options.reduce)
    print('Done\n')


if __name__ == '__main__':
    main()
