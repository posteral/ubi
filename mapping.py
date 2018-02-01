import json

import requests

import utils

def how_many_projects_in_env(env):
    projects = []
    uri = env.pp_base_uri() + '/projects'
    response = requests.get(uri)
    data = json.loads(response.text)
    print('Environment: '+str(env).split('.')[1])
    print('# of projects: '+str(len(data)))
    for project in data:
        projects.append((project['id'], project['name']))
    return projects

def how_many_mappings_in_project(project_name, project_id):
    return 10

#Get all mappings belonging to a project
#More info on the endpoint: http://doc.csq.io/project-parameters/#api-Mapping-getAll

TEST_ENV = utils.Env.NEXT2

projects = how_many_projects_in_env(TEST_ENV)

project_id = 269
pp_uri = TEST_ENV.pp_base_uri() + '/projects/' + str(project_id) + '/mappings'
print(pp_uri)
r = requests.get(pp_uri)
json_data = json.loads(r.text)


print('lala')


