import json

import requests

import utils

def get_projects_in_env(env):
    projects = []
    uri = env.pp_base_uri() + '/projects'
    response = requests.get(uri)
    data = json.loads(response.text)
    print('Environment: '+str(env).split('.')[1])
    print('# of projects: '+str(len(data)))
    for project in data:
        projects.append((project['id'], project['name']))
    return projects

def get_mappings_in_project(env, p_id, p_name):
    uri = env.pp_base_uri() + '/projects/' + str(p_id) + '/mappings'
    response = requests.get(uri)
    data = json.loads(response.text)
    print('# of mappings in project '+str(p_id)+' ('+p_name+'): '+str(len(data)))
    #@todo: return something

TEST_ENV = utils.Env.PRODUCTION

#projects = get_projects_in_env(TEST_ENV)
#
#for project in projects:
#    project_id = project[0]
#    project_name = project[1]
#    get_mappings_in_project(TEST_ENV, project_id, project_name)

file = open('stats/next2_mappings_per_project.txt','r')
file_lines = file.readlines()
number_of_projects = int(file_lines[1].split(': ')[1])
for project_line in file_lines[2:]:
    mappings_per_project = []
    line = project_line.replace('\n','').replace('((', '(').replace('))',')')
    print(line)
    substring_1 = line.split('(')[0].split(' ')
    substring_2 = line.split(')')[1].split(' ')
    project_name = line.split('(')[1].split(')')[0]
    project_id = int(substring_1[5])
    number_of_mappings = int(substring_2[1])

print(file_lines)
file.close()
