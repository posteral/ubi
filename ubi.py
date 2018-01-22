import json

import requests

import serviceConfig as cfg

#build URI from configuration file
uri = str(cfg.staging_config['host'])+':'+str(cfg.staging_config['port'])+str(cfg.routes['fetch-alert-configs'])
print(uri)

#fetch alerts
r = requests.post(uri)

#parse response
json_data = json.loads(r.text)

alert_es_parameters_array = json_data['alertESParametersArray']
print(alert_es_parameters_array)

#save in local db

uri = str(cfg.local_config['host'])+':'+str(cfg.local_config['port'])+str(cfg.routes['save-alert-esparameters'])
print(uri)

#save alert
alert = data = alert_es_parameters_array[0]
print(alert)

r = requests.post(uri, json = alert)

print(r)