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
    #return something

TEST_ENV = utils.Env.PRODUCTION

projects = get_projects_in_env(TEST_ENV)

for project in projects:
    project_id = project[0]
    project_name = project[1]
    get_mappings_in_project(TEST_ENV, project_id, project_name)

