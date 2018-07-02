import optparse
import os
import shutil
import subprocess
import json
from multiprocessing import Pool


from OSOL_Extremum.computational_core.unconstrained_optimization import *


def get_process_template(runner, algorithm):
    process = []

    if runner.endswith('jar'):
        process += ['java', '-jar', runner]
    elif runner.endswith('dll'):
        process += ['dotnet', runner]
    else:
        raise Exception('Unknown core')

    process += ['--algorithm', algorithm]
    process += ['--field', 'target']

    return process


def parse_result(f):
    j = json.load(open(f, 'r'))
    rv = j['RealVector']['elements']
    v = {}
    for kvp in rv:
        v[kvp['key']] = kvp['value']
    return v


def main():

    parser = optparse.OptionParser()
    parser.add_option('-A', '--algorithm',
                      help='Path to algorithm config',
                      type=str)
    parser.add_option('-R', '--runner',
                      help='Path to core',
                      type=str)
    parser.add_option('-T', '--tasks',
                      help='Path to folder with tasks',
                      type=str)
    parser.add_option('-N', '--number_of_runs',
                      help='Number of runs per tasks',
                      type=int)
    parser.add_option('-O', '--output',
                      help='Output folders',
                      type=str)
    parser.add_option('-P', '--port',
                      help='Running port',
                      type=int,
                      default=5017)
    parser.add_option('--parallel',
                      help='Number of parallel threads',
                      type=int,
                      default=1)

    options, _ = parser.parse_args()

    output_folder = options.output
    tasks_folder = options.tasks
    number_of_runs = options.number_of_runs
    port = options.port
    tasks = sorted(list(filter(lambda f: f.endswith('json'), os.listdir(tasks_folder))))

    process_base = get_process_template(options.runner, options.algorithm)

    print('>>> Preparing folder')
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    print('>>> Preparing processes')
    processes = []
    counter = 0
    for task_id, task in enumerate(tasks):
        task_name = task[:-5]
        for i in range(number_of_runs):
            p = process_base.copy()
            p += ['--task', tasks_folder + '/' + task]
            p += ['--port', str(port + counter)]
            p += ['--result', output_folder + '/{0}_{1}'.format(task_name, i + 1), '--output', 'json']
            processes.append(p)
            counter += 1

    print('>>> Running optimization tasks')
    pool = Pool(options.parallel)
    pool.map(subprocess.call, processes)
    pool.close()

    print('>>> Gathering statistics')
    results = {}
    for task_id, task in enumerate(tasks):
        task_name = task[:-5]
        core = UnconstrainedOptimization.from_dict(json.load(open(os.path.join(tasks_folder, task), 'r')))

        result_files = list(filter(lambda f: task_name in f, os.listdir(output_folder)))
        filtered_results = list(filter(lambda f: 'real' in f, result_files))
        if len(filtered_results) > 0:
            result_files = filtered_results

        results[task_name] = {'values': np.zeros(shape=(len(result_files), )), 'points': []}
        for i, rf in enumerate(result_files):
            x = parse_result(os.path.join(output_folder, rf))
            results[task_name]['points'].append(x)
            results[task_name]['values'][i] = core.f(x)
        results[task_name]['min'] = results[task_name]['values'].min()
        results[task_name]['mean'] = results[task_name]['values'].mean()
        results[task_name]['max'] = results[task_name]['values'].max()
        results[task_name]['std'] = results[task_name]['values'].std()
        results[task_name]['values'] = list(results[task_name]['values'])


    print('>>> Dumping result')
    json.dump(results, open(os.path.join(output_folder, 'statistics.json'), 'w'), indent=2)

    print('>>> Done!\n')


if __name__ == '__main__':
    main()
