import json

import requests

import serviceConfig as cfg

#build URI from configuration file
uri = str(cfg.staging_config['host'])+':'+str(cfg.staging_config['port'])+str(cfg.routes['fetch-alert-configs'])

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

response_array = []
for alert_configuration in alert_configuration_array:
    print(alert_configuration)
    r = requests.post(uri, json=alert_configuration)
    response_array.append(json.loads(r.text))
    print(r.json())


alert_confs_and_responses = zip(alert_configuration_array, response_array)

#check which values aren't in database and calculate them

metric_values = []

for alert_conf_and_response in alert_confs_and_responses:
    alert_conf = alert_conf_and_response[0]
    response = alert_conf_and_response[1]
    #check if time window 0 value is present in database
    time_window_0_value = response['timeWindow0Value']
    if time_window_0_value is None:
        uri = str(cfg.local_config['host'])+':'+str(cfg.local_config['port'])+str(cfg.routes['get-metric-value'])+'?timeWindow=timeWindow0'
        r = requests.post(uri, json=alert_conf)
        if r.status_code == 200: #success
            time_window_0_value = json.loads(r.text)['timeWindow0Value']
    # check if time window 0 value is present in database
    time_window_1_value = response['timeWindow1Value']
    if time_window_1_value is None:
        uri = str(cfg.local_config['host'])+':'+str(cfg.local_config['port'])+str(cfg.routes['get-metric-value'])+'?timeWindow=timeWindow1'
        r = requests.post(uri, json=alert_conf)
        if r.status_code == 200: #success
            time_window_1_value = json.loads(r.text)['timeWindow1Value']

    metric_values.append((time_window_0_value,time_window_1_value))


alert_confs_and_metric_values = zip(alert_configuration_array, metric_values)

# save metric values in local db

for alert_conf_and_metric_values in alert_confs_and_metric_values:
    alert_conf = alert_conf_and_metric_values[0]
    metric_values = alert_conf_and_metric_values[1]
    #save metric value for time window 0
    if metric_values[0] is not None:
        uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(cfg.routes['save-metric-value']) + \
              '?timeWindow=timeWindow0&value='+str(metric_values[0])
        r = requests.post(uri, json=alert_conf)
    if metric_values[1] is not None:
        uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(cfg.routes['save-metric-value']) + \
              '?timeWindow=timeWindow1&value='+str(metric_values[1])
        r = requests.post(uri, json=alert_conf)

