from argparse import ArgumentParser, RawTextHelpFormatter
from multiprocessing import Pool

import os
import shutil
import subprocess


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
        print(len(task_files))
        task_files = [f for f in task_files if f not in already_processed]
        print(len(task_files))

    pool = Pool(args.max_processes)
    if mode == 'first':
        process_args = [(alg_config, source_folder, t, 5017 + i, target_folder) for i, t in enumerate(task_files)]
        pool.map(run_process_1, process_args)
    elif mode == 'second':
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

parser.add_argument('--target_folder',
                    type=str,
                    help='Folder with tasks')

parser.add_argument('--max_processes',
                    type=int,
                    default=8,
                    help='Number of parallel threads')


args = parser.parse_args()

main(args)
