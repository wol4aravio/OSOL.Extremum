from argparse import ArgumentParser, RawTextHelpFormatter
from multiprocessing import Pool

from OSOL_Extremum.arithmetics.interval import Interval

import os
import shutil
import subprocess
import json

import numpy as np


def run_process_1(args):
    alg_config, from_folder, task, port, to_folder = args
    task_id = task[:-5]

    process = []
    process += ['java', '-jar', '{}/OSOL.Extremum.Apps.JVM.Runner.jar'.format(os.environ['JVM_RUNNER'])]
    process += ['--algorithm', alg_config]
    process += ['--task', from_folder + '/' + task]
    process += ['--port', str(port)]
    process += ['--field', 'sim']
    process += ['--result', to_folder + '/' + task_id, '--output', 'json']
    # process += ['--log-states', logs_dir]

    subprocess.call(process)

    return


def run_process_2(args):
    alg_config, from_folder, task, seed_folder, seed, port, to_folder = args
    task_id = task[:-5]

    process = []
    process += ['java', '-jar', '{}/OSOL.Extremum.Apps.JVM.Runner.jar'.format(os.environ['JVM_RUNNER'])]
    process += ['--algorithm', alg_config]
    process += ['--task', from_folder + '/' + task]
    process += ['--port', str(port)]
    process += ['--field', 'sim']
    process += ['--seed', seed_folder + '/' + seed]
    process += ['--result', to_folder + '/' + task_id, '--output', 'json']
    # process += ['--log-states', logs_dir]

    subprocess.call(process)

    return


def convert(e, points=np.linspace(0, 1, 11)):
    coeffs = dict([(kvp['key'], Interval.from_dict(kvp['value'])) for kvp in e['IntervalVector']['elements']])
    u1 = lambda t: coeffs['a1'] + coeffs['b1'] * t + coeffs['c1'] * t * t
    u2 = lambda t: coeffs['a2'] + coeffs['b2'] * t + coeffs['c2'] * t * t
    u3 = lambda t: coeffs['a3'] + coeffs['b3'] * t + coeffs['c3'] * t * t
    u = {'u1': u1, 'u2': u2, 'u3': u3}
    new_coeffs = []
    for i, p in enumerate(points):
        for u_name, u_func in u.items():
            new_coeffs.append({'key': '{0}_{1}'.format(u_name, i), 'value': u_func(p)})
    new_e = e.copy()
    new_e['IntervalVector']['elements'] = new_coeffs
    return new_e


def modify_seed(seed_loc, seed_file, target_loc):
    seed = json.load(open(seed_loc + '/' + seed_file, 'r'))
    new_seed = [convert(s) for s in seed]
    json.dump(new_seed, open(target_loc + '/' + seed_file, 'w'))
    return


def main(args):
    mode = args.mode
    resume = args.resume
    alg_config = args.alg_config
    source_folder = args.source_folder
    target_folder = args.target_folder

    if os.path.exists(target_folder):
        if not resume:
            shutil.rmtree(target_folder)
            os.makedirs(target_folder)
    else:
        os.makedirs(target_folder)

    task_files = sorted(list(filter(lambda f: f.endswith('json'), os.listdir(source_folder))))
    if resume:
        already_processed = list(filter(lambda f: f.endswith('json') and ('seed' not in f) and ('real' not in f),
                                        os.listdir(target_folder)))
        already_processed = sorted(already_processed)
        task_files = [f for f in task_files if f not in already_processed]

    pool = Pool(args.max_processes)
    if mode == 'first':
        process_args = [(alg_config, source_folder, t, 5017 + i, target_folder) for i, t in enumerate(task_files)]
        pool.map(run_process_1, process_args)
    elif mode == 'second':
        seed_folder = args.seed_folder
        seed_files = sorted(list(filter(lambda f: f.endswith('json') and ('seed' in f), os.listdir(seed_folder))))
        for s in seed_files:
            modify_seed(seed_folder, s, target_folder)

        process_args = [(alg_config, source_folder, t, target_folder, list(filter(lambda f: t[:-5] in f, seed_files))[0], 5017 + i, target_folder) for i, t in enumerate(task_files)]
        pool.map(run_process_2, process_args)

        return
    else:
        pool.close()
        raise Exception('Unsupported mode')
    pool.close()


parser = ArgumentParser(description='Runner', formatter_class=RawTextHelpFormatter)

parser.add_argument('--mode',
                    type=str,
                    help='Working mode')

parser.add_argument('--resume',
                    action='store_true',
                    default=False,
                    help='Resume cancelled calculation')

parser.add_argument('--alg_config',
                    type=str,
                    help='Path to algorithm config')

parser.add_argument('--source_folder',
                    type=str,
                    help='Folder with tasks')

parser.add_argument('--seed_folder',
                    type=str,
                    help='Folder with seed tasks')

parser.add_argument('--target_folder',
                    type=str,
                    help='Folder with tasks')

parser.add_argument('--max_processes',
                    type=int,
                    default=8,
                    help='Number of parallel threads')


args = parser.parse_args()

main(args)
