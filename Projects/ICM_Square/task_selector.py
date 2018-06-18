from argparse import ArgumentParser, RawTextHelpFormatter

import os
import shutil

import pandas as pd
import numpy as np


def main(args):
    source_folder = args.source_folder
    query = args.query
    target_folder = args.target_folder

    legend = pd.read_csv(source_folder + '/legend.csv',
                         index_col=None,
                         dtype={'p0': np.float, 'q0': np.float, 'r0': np.float, 'name': np.str})
    legend = legend.query(query)

    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    os.makedirs(target_folder)

    for f in legend['name'].values:
        shutil.copyfile('{0}/{1}.json'.format(source_folder, f), '{0}/{1}.json'.format(target_folder, f))
    legend.to_csv(target_folder + '/legend.csv', index=False)
    with open(target_folder + '/query.txt', 'w') as query_text:
        query_text.write(query + '\n')

    return


parser = ArgumentParser(description='Data Selector', formatter_class=RawTextHelpFormatter)

parser.add_argument('--query',
                    type=str,
                    help='Selecting query')

parser.add_argument('--source_folder',
                    type=str,
                    help='Folder with tasks')

parser.add_argument('--target_folder',
                    type=str,
                    help='Folder to store selected tasks')

args = parser.parse_args()

main(args)
