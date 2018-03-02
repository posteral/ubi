import json

import requests


projectId = 88      #Cdiscount
mappingId = 7670    #AB - Matelas
pageId = 106558     #Matelas
number_of_results = 20
fov1 = '{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"filter"}'
fov2 = '{"nodeType":"AND","children":[{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"filter"}, {"field":"page:path","operator":"not_contains","value":"-2.html","nodeType":"filter"}]}'
fov3 = '{"nodeType":"AND","children":[{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"filter"}, {"field":"page:path","operator":"contains","value":"-2.html","nodeType":"NOT"}]}'
fov4 = '{"field":"page:path","operator":"contains","value":"l-1175520","nodeType":"NOT"}'

base_uri = 'http://localhost:8080'
path ='/pagecarto/v1/projects/'+str(projectId)+'/search?'


query_parameters = 'mappingId='+str(mappingId)+'&groupBy=path&order=desc&pageId='+str(pageId)+'&range=0,'+str(number_of_results)

###########################################################
parsed = json.loads(fov1)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + fov1
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))


###########################################################
parsed = json.loads(fov2)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + fov2
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))

###########################################################
parsed = json.loads(fov3)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + fov3
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))

###########################################################
parsed = json.loads(fov4)
print(json.dumps(parsed, indent=4, sort_keys=False))
url = base_uri + path + query_parameters + '&filter=' + fov4
print(url)

response = requests.get(url)
data = json.loads(response.text)

print(data)
print(len(data))

stringTest = """{"timestamp":"2017-07-17T21:23:54.110Z","dep_version":"$depv","dep_region":"unknown","tag_version":"2.3.7","project_id":331,"path":"/pageview","user_id":"4ce6e0d4-9a87-a498-e231-5d4ea352c5e4","session_number":1,"page_number":3,"returning":false,"recorded":0,"country":"United Kingdom","country_code":"GB","browserName":"Mobile Safari","browserVersion":"7.0","browserType":"Browser (mobile)","deviceType":"Mobile","platformName":"iOS 7 (iPhone)","deviceManufacturer":"Apple Inc.","enrichmentVersion":"collect-monitoring-${BuildInfo.version}"}"""
parsed = json.loads(stringTest)
parsedFinal = json.dumps(parsed, indent=4, sort_keys=False)

print("hello")

