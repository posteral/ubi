import json

import urllib.parse
import requests


projectId = 88      #Cdiscount
mappingId = 7670    #AB - Matelas
pageId = 106558     #Matelas
number_of_results = 20

#select * from project_page_alias where project_page_alias.project_id = 88 and project_page_alias.id = 106558;

page_target = '{"nodeType":"OR","children":[{"nodeType":"AND","children":[{"field":"page:path","operator":"not_contains","value":".html","nodeType":"filter"}]}]}'
parsed = json.loads(page_target)

print(json.dumps(parsed, indent=4, sort_keys=False))

fov1 = '{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"filter"}'
fov2 = '{"nodeType":"AND","children":[{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"filter"}, {"field":"page:path","operator":"not_contains","value":"-2.html","nodeType":"filter"}]}'
fov3 = '{"nodeType":"AND","children":[{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"filter"}, {"field":"page:path","operator":"contains","value":"-2.html","nodeType":"NOT"}]}'
fov4 = '{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"NOT"}'

base_uri = 'http://hpg-pagecarto-next2.csq.io:8080'
path ='/pagecarto/v1/projects/'+str(projectId)+'/search?'


query_parameters = 'mappingId='+str(mappingId)+'&groupBy=path&order=desc&pageId='+str(pageId)+'&range=0,'+str(number_of_results)

###########################################################
parsed = json.loads(fov1)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + urllib.parse.quote_plus(fov1)
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))


###########################################################
parsed = json.loads(fov2)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + urllib.parse.quote_plus(fov2)
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))

###########################################################
parsed = json.loads(fov3)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + urllib.parse.quote_plus(fov3)
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))

###########################################################
parsed = json.loads(fov4)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + urllib.parse.quote_plus(fov4)
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))


