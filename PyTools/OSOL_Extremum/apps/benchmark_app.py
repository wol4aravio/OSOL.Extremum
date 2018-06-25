import optparse
import os
import shutil
import subprocess


def get_process_template(core, algorithm, port):
    process = []

    if core.endswith('jar'):
        process += ['java', '-jar', core]
    elif core.endswith('dll'):
        process += ['dotnet', core]
    else:
        raise Exception('Unknown core')

    process += ['--algorithm', algorithm]
    process += ['--port', str(port)]
    process += ['--field', 'f']

    return process


def main():

    parser = optparse.OptionParser()
    parser.add_option('-A', '--algorithm',
                      help='Path to algorithm config',
                      type=str)
    parser.add_option('-C', '--core',
                      help='Path to core',
                      type=str)
    parser.add_option('-T', '--tasks',
                      help='Path to folder with tasks',
                      type=str)
    parser.add_option('-R', '--runs',
                      help='Number of runs per tasks',
                      type=int)
    parser.add_option('-O', '--output',
                      help='Output folders',
                      type=str)
    parser.add_option('-P', '--port',
                      help='Running port',
                      type=int,
                      default=5017)

    options, _ = parser.parse_args()

    process_base = get_process_template(options.core, options.algorithm, options.port)

    if os.path.exists(options.output):
        shutil.rmtree(options.output)
    os.makedirs(options.output)

    tasks = sorted(os.listdir(options.tasks))
    for task_id, task in enumerate(tasks):
        print('Processing {0} ({1}/{2})'.format(task, task_id + 1, len(tasks)))
        task_name = task[:-5]
        for i in range(options.runs):
            print('>>> Run {0}/{1}'.format(i + 1, options.runs))
            p = process_base.copy()
            p += ['--task', options.tasks + '/' + task]
            p += ['--result', options.output + '/{0}_{1}'.format(task_name, i + 1), '--output', 'json']
            subprocess.call(p)


if __name__ == '__main__':
    main()
