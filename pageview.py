import json
import time

import requests

import env

TEST_ENV = env.Env.STAGING

#let's find out whose projects have the biggest pageview count



file = open(TEST_ENV.mappings_file(),'r')
file_lines = file.readlines()
total_number_of_projects = int(file_lines[1].split(': ')[1])
pageviews_in_projects = []
for project_line in file_lines[2:]:
    line = project_line.replace('\n','').replace('((', '(').replace('))',')')
    substring_1 = line.split('(')[0].split(' ')
    substring_2 = line.split(')')[1].split(' ')
    project_name = line.split('(')[1].split(')')[0]
    project_id = int(substring_1[5])
    # we're going to use hpg-dashboard to obtain ES results
    uri = TEST_ENV.dashboard_base_uri() + \
          '/dashboard/v1/projects/' + str(project_id) + '/metrics?' \
          'goalId=-1' \
          '&segmentIds=-1' \
          '&segmentInclude=true' \
          '&deviceId=-1' \
          '&from=2018-02-14T00:00:00Z' \
          '&to=2018-02-14T23:22:59Z' \
          '&isEcommerce=true'
    response = requests.get(uri)
    if response.status_code == 200:
        data = json.loads(response.text)
        pageviews = data['visitCount']
        print(str(project_id) + ' ' + project_name + ' ' + str(pageviews))
        pageviews_in_projects.append((project_id, project_name, pageviews))
    time.sleep(0.5)

sorted_by_number_of_mappings = sorted(pageviews_in_projects, key=lambda tup: tup[2], reverse=True)
print('Projects with most pageviews: '+str(sorted_by_number_of_mappings))




print()