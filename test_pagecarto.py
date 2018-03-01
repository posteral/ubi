import json

import requests


projectId = 88
mappingId = 7033
pageId = 31812
number_of_results = 20
fov = '{"nodeType":"OR","children":[{"nodeType":"AND","children":[{"field":"page:path","operator":"contains","value":"/recherche","nodeType":"filter"}]}]}'

base_uri = 'http://localhost:8080'
path ='/pagecarto/v1/projects/'+str(projectId)+'/search?'


parsed = json.loads(fov)
print(json.dumps(parsed, indent=4, sort_keys=False))

query_parameters = 'mappingId='+str(mappingId)+'&groupBy=path&order=desc&pageId='+str(pageId)+'&range=0,'+str(number_of_results)+'&filter='+fov

url = base_uri + path + query_parameters


response = requests.get(url)
data = json.loads(response.text)

print(data)