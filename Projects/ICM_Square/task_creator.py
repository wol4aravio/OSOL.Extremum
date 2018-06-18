import os
import shutil
import json

import numpy as np
import pandas as pd


def make_tasks(task_template, initials, u_min, u_max, location):
    cur_dir = os.getcwd()
    new_area = []
    for l in ['a', 'b', 'c']:
        for i in range(1, 4):
            new_area.append({'name': '{0}{1}'.format(l, i), 'min': u_min, 'max': u_max})

    start_config = []
    for p_init in np.linspace(initials['p']['min'], initials['p']['max'], initials['p']['N']).tolist():
        for q_init in np.linspace(initials['q']['min'], initials['q']['max'], initials['q']['N']).tolist():
            for r_init in np.linspace(initials['r']['min'], initials['r']['max'], initials['r']['N']).tolist():
                start_config.append([
                    {'name': 'p', 'value': p_init},
                    {'name': 'q', 'value': q_init},
                    {'name': 'r', 'value': r_init}
                ])
    start_config = dict([('{0:07d}'.format(id + 1), inits) for id, inits in enumerate(start_config)])

    if os.path.exists(cur_dir + '/' + location):
        shutil.rmtree(location)
    os.makedirs(location)

    for task_id, initial_conditions in start_config.items():
        temp_task = task_template.copy()
        temp_task['area'] = new_area
        temp_task['initial_conditions'] = initial_conditions
        for i in range(0, 3):
            temp_task['control_bounds'][i]['min'] = u_min
            temp_task['control_bounds'][i]['max'] = u_max
        json.dump(temp_task, open(cur_dir + '/' + location + '/{}.json'.format(task_id), 'w'), indent=4)

    legend = [[v['value'] for v in values] + [file_name] for file_name, values in start_config.items()]
    legend = pd.DataFrame(data=legend, columns=['p0', 'q0', 'r0', 'name'])
    legend.to_csv(cur_dir + '/' + location + '/legend.csv', index=False)
    return


initial_values = {
    'p': {'min': -25.0, 'max': 25.0, 'N': 51},
    'q': {'min': -25.0, 'max': 25.0, 'N': 51},
    'r': {'min': -25.0, 'max': 25.0, 'N': 51}
}

if os.path.exists('tasks_1'):
    shutil.rmtree('tasks_1')
make_tasks(task_template=json.load(open('TaskTemplateExplicit.json', 'r')),
           initials=initial_values, u_min=-500, u_max=500, location='tasks_1')

if os.path.exists('tasks_2'):
    shutil.rmtree('tasks_2')
make_tasks(task_template=json.load(open('TaskTemplate.json', 'r')),
           initials=initial_values, u_min=-500, u_max=500, location='tasks_2')

print('Done')
