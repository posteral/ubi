import json

import requests

import env

import serviceConfig as cfg

TEST_ENV = env.Env.NEXT2

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

#projects = get_projects_in_env(TEST_ENV)
#
#for project in projects:
#    project_id = project[0]
#    project_name = project[1]
#    get_mappings_in_project(TEST_ENV, project_id, project_name)

file = open(TEST_ENV.mappings_file(),'r')
file_lines = file.readlines()
total_number_of_projects = int(file_lines[1].split(': ')[1])
mappings_in_projects = []
for project_line in file_lines[2:]:
    line = project_line.replace('\n','').replace('((', '(').replace('))',')')
    #print(line)
    substring_1 = line.split('(')[0].split(' ')
    substring_2 = line.split(')')[1].split(' ')
    project_name = line.split('(')[1].split(')')[0]
    project_id = int(substring_1[5])
    number_of_mappings = int(substring_2[1])
    mappings_in_projects.append((project_id, project_name, number_of_mappings))

print('# projects in '+str(TEST_ENV).split('.')[1]+': '+str(total_number_of_projects))
#now we have the list of projects and their respective number of mappings
more_than_zero_mappings = []

for mappings_in_project in mappings_in_projects:
    if mappings_in_project[2] > 0:
        more_than_zero_mappings.append(mappings_in_project)

print('# projects with more than 0 mappings: '+str(len(more_than_zero_mappings)))

total_number_of_mappings_in_environment = 0
for mappings_in_project in more_than_zero_mappings:
    total_number_of_mappings_in_environment = total_number_of_mappings_in_environment + mappings_in_project[2]

print('# of mappings in environment: '+str(total_number_of_mappings_in_environment))
average_mappings_per_project = total_number_of_mappings_in_environment/len(more_than_zero_mappings)
print('# of average mappings per project: '+str(average_mappings_per_project))

sorted_by_number_of_mappings = sorted(more_than_zero_mappings, key=lambda tup: tup[2], reverse=True)
print('Projects with most mappings: '+str(sorted_by_number_of_mappings))

#what's the average number of aliases per mapping?
#let's use hypergate to find out

inconsistencies = 0
avg_nb_aliases_per_mapping_in_projects = []
for mappings_in_project in more_than_zero_mappings:
    project_id = mappings_in_project[0]
    project_name = mappings_in_project[1]
    nb_mappings_on_pp = mappings_in_project[2]
    uri = TEST_ENV.hpg_base_uri() + '/project-settings/v1/projects/'+str(project_id)+'/mappings'
    response = requests.get(uri, headers=cfg.hpg_headers)
    data = json.loads(response.text)
    mappings = data['mappings']
    #checking pp / hpg inconsistencies
    if nb_mappings_on_pp != len(mappings):
        inconsistencies = inconsistencies + 1
    if len(mappings) > 0 :
        total_number_of_aliases = 0
        for mapping in mappings:
            number_of_aliases = int(len(mapping['aliasesIds']))
            total_number_of_aliases = total_number_of_aliases + number_of_aliases
            avg_nb_aliases_per_mapping = total_number_of_aliases/len(mappings)
            avg_nb_aliases_per_mapping_in_projects.append((project_id, project_name, avg_nb_aliases_per_mapping))
            #print(avg_nb_aliases_per_mapping)

print("# inconsistencies pp/hpg: "+str(inconsistencies))
average_sum = 0
for avg in avg_nb_aliases_per_mapping_in_projects:
    average_sum = average_sum + avg[2]

avg_aliases_per_mapping_per_project_in_env = average_sum/len(avg_nb_aliases_per_mapping_in_projects)

print("# of average aliases per mapping in a project: "+str(avg_aliases_per_mapping_per_project_in_env))

file.close()
