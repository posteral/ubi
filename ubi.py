import json

import requests

import serviceConfig as cfg

#build URI from configuration file
uri = str(cfg.staging_config['host'])+':'+str(cfg.staging_config['port'])+str(cfg.routes['fetch-alert-configs'])
print(uri)

#query service
r = requests.post(uri)

#parse response
json_data = json.loads(r.text)

alert_es_parameters_array = json_data['alertESParametersArray']

print(alert_es_parameters_array)