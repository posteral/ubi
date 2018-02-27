file = open('stats/sorted_by_pageviews','r')
file_lines = file.readlines()
data = file_lines[0].replace(')','').split(", (") #we just have one line

for project_pageviews in data:
    split = project_pageviews.replace('(','').split(',')
    project_id =  int(split[0])
    project_name = split[1]
    pageviews = int(split[2])

    print(str(project_id)+';'+project_name+';'+str(pageviews))