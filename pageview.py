import env

TEST_ENV = env.Env.STAGING

#let's find out whose projects have the biggest pageview count

file = open(TEST_ENV.mappings_file(),'r')
file_lines = file.readlines()
total_number_of_projects = int(file_lines[1].split(': ')[1])
mappings_in_projects = []
for project_line in file_lines[2:]:
    line = project_line.replace('\n','').replace('((', '(').replace('))',')')
    substring_1 = line.split('(')[0].split(' ')
    substring_2 = line.split(')')[1].split(' ')
    project_name = line.split('(')[1].split(')')[0]
    project_id = int(substring_1[5])
    print(str(project_id)+' '+project_name)