import json

import requests

import endpoints
import serviceConfig as cfg
import utils

INPUT_ENV = utils.Env.STAGING
TEST_ENV = utils.Env.LOCAL

# fetch alerts
r = endpoints.fetchAlertConfigs(INPUT_ENV)

# parse response
json_data = json.loads(r.text)

alert_es_parameters_array = json_data['alertESParametersArray']
alert_configuration_array = json_data['alertConfigurationArray']

print('-------------------------------------------------------')
print('# AlertESParameters: ' + str(len(alert_es_parameters_array)))
print('# AlertConfigurations (different alerts): ' + str(len(alert_configuration_array)))
print('-------------------------------------------------------')

# save alert-es-parameters in local db

uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(cfg.routes['save-alert-esparameters'])

for alert_es_parameters in alert_es_parameters_array:
    r = requests.post(uri, json=alert_es_parameters, timeout=10)

hpg_requests = 0
# try to calculate metric values for alert configuration

uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(cfg.routes['get-metric-values'])

response_array = []

for idx, alert_configuration in enumerate(alert_configuration_array):
    r = requests.post(uri, json=alert_configuration, timeout=10)
    metric_values = json.loads(r.text)
    response_array.append(metric_values)
    print(str(idx + 1) + '\t alertId: ' + str(alert_configuration['alertId']) + ', ' + str(metric_values))

alert_confs_and_responses = zip(alert_configuration_array, response_array)

metric_values = []

# let's try to identify where the problems are
problems = []

# check which values aren't in database and calculate them
for alert_conf_and_response in alert_confs_and_responses:
    alert_conf = alert_conf_and_response[0]
    response = alert_conf_and_response[1]
    # check if time window 0 value is present in database
    time_window_0_value = response['timeWindow0Value']
    if time_window_0_value is None:
        uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(
            cfg.routes['get-metric-value']) + '?timeWindow=timeWindow0'
        r = requests.post(uri, json=alert_conf, timeout=10)
        hpg_requests = hpg_requests + 1
        if r.status_code == 200:  # success
            time_window_0_value = json.loads(r.text)['timeWindow0Value']
        else:
            problems.append((r.status_code, uri, alert_conf))
    # check if time window 0 value is present in database
    time_window_1_value = response['timeWindow1Value']
    if time_window_1_value is None:
        uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(
            cfg.routes['get-metric-value']) + '?timeWindow=timeWindow1'
        r = requests.post(uri, json=alert_conf, timeout=10)
        hpg_requests = hpg_requests + 1
        if r.status_code == 200:  # success
            time_window_1_value = json.loads(r.text)['timeWindow1Value']
        else:
            problems.append((r.status_code, uri, alert_conf))

    metric_values.append((time_window_0_value, time_window_1_value))

print('\n-----------------PROBLEMS-----------------------')
for idx, problem in enumerate(problems):
    print('Problem ' + str(
        idx + 1) + ': $\n\t' + "curl --request POST --url '" + uri + "' --header 'content-type: application/json' --data '" + str(
        problem[2]).replace("\'", "\"") + "' -i")
print('------------------------------------------------')

print('\n# of hpg-requests (ES queries) needed: ' + str(hpg_requests))
alert_confs_and_metric_values = zip(alert_configuration_array, metric_values)

# save metric values in local db

for alert_conf_and_metric_values in alert_confs_and_metric_values:
    alert_conf = alert_conf_and_metric_values[0]
    metric_values = alert_conf_and_metric_values[1]
    # save metric value for time window 0
    if metric_values[0] is not None:
        uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(
            cfg.routes['save-metric-value']) + \
              '?timeWindow=timeWindow0&value=' + str(metric_values[0])
        r = requests.post(uri, json=alert_conf, timeout=10)
    if metric_values[1] is not None:
        uri = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port']) + str(
            cfg.routes['save-metric-value']) + \
              '?timeWindow=timeWindow1&value=' + str(metric_values[1])
        r = requests.post(uri, json=alert_conf, timeout=10)
