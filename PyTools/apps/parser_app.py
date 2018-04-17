import sys
import os

cwd = os.getcwd()
sys.path.insert(0, cwd)
sys.path.insert(0, cwd[:cwd.rindex('/')])
sys.path.insert(0, cwd + '/temp')

from argparse import ArgumentParser, RawTextHelpFormatter
from parser.parser import parse_to_tree


def main(args):
    result = parse_to_tree("".join(args.function))
    print(result)


parser = ArgumentParser(description="Parser App", formatter_class=RawTextHelpFormatter)

parser.add_argument("--function",
                    type=str,
                    nargs="+",
                    help='Function to be parsed')

args = parser.parse_args()

main(args)
