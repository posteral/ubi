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

response_array = []
for alert_configuration in alert_configuration_array:
    print(alert_configuration)
    r = requests.post(uri, json=alert_configuration)
    response_array.append(json.loads(r.text))
    print(r.json())


alert_confs_and_responses = zip(alert_configuration_array, response_array)

#check which values aren't in database and calculate them

for alert_conf_and_response in alert_confs_and_responses:
    alert_conf = alert_conf_and_response[0]
    response = alert_conf_and_response[1]
    time_window_0_value = response['timeWindow0Value']
    time_window_1_value = response['timeWindow1Value']
    print("oi")