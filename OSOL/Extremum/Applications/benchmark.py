import os
import sys

sys.path.append(os.getcwd())

from OSOL.Extremum.Tools.Encoders import CustomEncoder
from OSOL.Extremum.Optimization.Tasks.UnconstrainedOptimization import UnconstrainedOptimization
from OSOL.Extremum.Numerical_Objects.Vector import Vector

import optparse
import shutil
import subprocess
from joblib import Parallel, delayed
import json
from grip import export
import numpy as np


def get_process_template(algorithm, terminator):
    process = ['python', 'OSOL/Extremum/Applications/optimize.py',
               '-A', algorithm,
               '-T', terminator]
    return process


def create_markdown(results):
    text = '''**Benchmark results (detailed)**

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
'''
    for f_name, stat in results.items():
        text += '| {0} | {1:.9f} | {2:.9f} | {3:.9f} | {4:.9f} | {5:.9f} |\n'.format(
            f_name, stat['f*'], stat['min'], stat['mean'], stat['max'], stat['std'])

    text += '''
**Benchmark results**

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
'''
    for f_name, stat in results.items():
        text += '| {0} | {1:.5f} | {2:.5f} | {3:.5f} | {4:.5f} | {5:.5f} |\n'.format(
            f_name, stat['f*'], stat['min'], stat['mean'], stat['max'], stat['std'])

    return text


def create_tex(results):
    text = '''Benchmark results (detailed)
\\begin{tabular}{|l|c|c|c|c|c|}
\\hline
Function name & Optimal value & Min value & Mean value & Max value & Standard deviation \\\\ \\hline
'''
    for f_name, stat in results.items():
        text += '{0} & ${1:.9f}$ & ${2:.9f}$ & ${3:.9f}$ & ${4:.9f}$ & ${5:.9f}$ \\\\ \\hline \n'.format(
            f_name, stat['f*'], stat['min'], stat['mean'], stat['max'], stat['std'])
    text += '\\end{tabular} \n\n'

    text += '''Benchmark results
\\begin{tabular}{|l|c|c|c|c|c|}
\\hline
Function name & Optimal value & Min value & Mean value & Max value & Standard deviation \\\\ \\hline
'''
    for f_name, stat in results.items():
        text += '{0} & ${1:.5f}$ & ${2:.5f}$ & ${3:.5f}$ & ${4:.5f}$ & ${5:.5f}$ \\\\ \\hline \n'.format(
            f_name, stat['f*'], stat['min'], stat['mean'], stat['max'], stat['std'])
    text += '\\end{tabular} \n\n'

    return text


def main():

    parser = optparse.OptionParser()
    parser.add_option('-A', '--algorithm',
                      help='Path to algorithm config',
                      type=str)
    parser.add_option('-W', '--working_time',
                      help='Algorithm working time',
                      type=str)
    parser.add_option('-T', '--tasks',
                      help='Path to folder with tasks',
                      type=str)
    parser.add_option('-R', '--number_of_runs',
                      help='Number of runs per tasks',
                      type=int)
    parser.add_option('-O', '--output',
                      help='Output folders',
                      type=str)
    parser.add_option('--parallel',
                      help='Number of parallel threads',
                      type=int,
                      default=1)

    options, _ = parser.parse_args()

    output_folder = options.output
    tasks_folder = options.tasks
    number_of_runs = options.number_of_runs
    result_folder = os.path.join(output_folder, 'results')
    tasks = sorted(list(
        filter(lambda f: f.endswith('json'),
               os.listdir(tasks_folder))))

    process_base = get_process_template(options.algorithm, options.working_time)

    print('>>> Preparing folder')
    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)
    os.makedirs(result_folder)

    print('>>> Preparing processes')
    processes = []
    counter = 0
    for _, task in enumerate(tasks):
        task_name = task[:-5]
        for i in range(number_of_runs):
            p = process_base.copy()
            p += ['-P', tasks_folder + '/' + task]
            p += ['-O', os.path.join(result_folder, '{0}_{1}.json'.format(task_name, i + 1))]
            processes.append(p)
            counter += 1

    print('>>> Running optimization tasks')
    Parallel(n_jobs=options.parallel)(delayed(subprocess.call)(p)
                                      for p in processes)

    print('>>> Gathering statistics')
    results = {}
    for task_id, task in enumerate(tasks):
        task_name = task[:-5]
        task_json = json.load(open(os.path.join(tasks_folder, task), 'r'))
        x_best = {}
        for kvp in task_json['solution']:
            x_best[kvp['name']] = kvp['value']
        x_best = Vector(x_best)
        f = UnconstrainedOptimization(
            f=task_json['f'],
            variables=task_json['vars'])

        result_files = list(
            filter(lambda f: task_name in f, os.listdir(result_folder)))
        filtered_results = sorted(
            list(filter(lambda f: 'real' in f, result_files)))
        if len(filtered_results) > 0:
            result_files = filtered_results

        results[task_name] = {'values': np.zeros(shape=(len(result_files), )), 'points': [],
                              'x*': x_best, 'f*': f(x_best)}
        for i, rf in enumerate(result_files):
            x = Vector.from_json(
                json.load(open(os.path.join(result_folder, rf), 'r')))
            results[task_name]['points'].append(x)
            results[task_name]['values'][i] = f(x)

        results[task_name]['min'] = results[task_name]['values'].min()
        results[task_name]['mean'] = results[task_name]['values'].mean()
        results[task_name]['max'] = results[task_name]['values'].max()
        results[task_name]['std'] = results[task_name]['values'].std()
        results[task_name]['values'] = list(results[task_name]['values'])

    print('>>> Dumping result')
    shutil.copyfile(options.algorithm, os.path.join(
        output_folder, 'config.json'))
    json.dump(results,
              open(os.path.join(output_folder, 'statistics.json'), 'w'), cls=CustomEncoder, indent=2)
    md = create_markdown(results)
    with open(os.path.join(output_folder, 'statistics.md'), 'w') as md_file:
        md_file.write(md)
    export(path=os.path.join(output_folder, 'statistics.md'))
    with open(os.path.join(output_folder, 'for_tex.txt'), 'w') as tex_file:
        tex_file.write(create_tex(results))

    print('>>> Done!\n')


if __name__ == '__main__':
    main()
