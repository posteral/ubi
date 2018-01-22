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
alert_configuration_array = json_data['alertConfigurationArray']

#save in local db

uri = str(cfg.local_config['host'])+':'+str(cfg.local_config['port'])+str(cfg.routes['save-alert-esparameters'])

for alert_es_parameters in alert_es_parameters_array:
    print(alert_es_parameters)
    r = requests.post(uri, json=alert_es_parameters)
    print(r)

#try to get metric values for alert configuration

uri = str(cfg.local_config['host'])+':'+str(cfg.local_config['port'])+str(cfg.routes['get-metric-values'])
print(uri)

for alert_configuration in alert_configuration_array:
    print(alert_configuration)
    r = requests.post(uri, json=alert_configuration)
    print(r.json())
