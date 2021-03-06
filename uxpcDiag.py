import json

import requests

import endpoints
import serviceConfig as cfg
import env

TIME_OUT = 30
NOTIFICATIONS = False
INPUT_ENV = env.Env.NEXT2
TEST_ENV = env.Env.LOCAL

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

uri = TEST_ENV.uxpc_base_uri() + str(cfg.routes['save-alert-esparameters'])

for alert_es_parameters in alert_es_parameters_array:
    r = requests.post(uri, json=alert_es_parameters, timeout=TIME_OUT)

hpg_requests = 0
# try to calculate metric values for alert configuration

uri = TEST_ENV.uxpc_base_uri() + str(cfg.routes['get-metric-values'])

response_array = []

for idx, alert_configuration in enumerate(alert_configuration_array):
    r = requests.post(uri, json=alert_configuration, timeout=TIME_OUT)
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
        uri = TEST_ENV.uxpc_base_uri() + str(
            cfg.routes['get-metric-value']) + '?timeWindow=timeWindow0'
        r = requests.post(uri, json=alert_conf, timeout=TIME_OUT)
        hpg_requests = hpg_requests + 1
        if r.status_code == 200:  # success
            time_window_0_value = json.loads(r.text)['timeWindow0Value']
        else:
            problems.append((r.status_code, uri, alert_conf))
    # check if time window 0 value is present in database
    time_window_1_value = response['timeWindow1Value']
    if time_window_1_value is None:
        uri = TEST_ENV.uxpc_base_uri() + str(
            cfg.routes['get-metric-value']) + '?timeWindow=timeWindow1'
        r = requests.post(uri, json=alert_conf, timeout=TIME_OUT)
        hpg_requests = hpg_requests + 1
        if r.status_code == 200:  # success
            time_window_1_value = json.loads(r.text)['timeWindow1Value']
        else:
            problems.append((r.status_code, uri, alert_conf))

    metric_values.append((time_window_0_value, time_window_1_value))


print('\n# of hpg-requests (ES queries) needed: ' + str(hpg_requests))
alert_confs_and_metric_values = zip(alert_configuration_array, metric_values)


# save metric values in local db and notify

for alert_conf_and_metric_values in alert_confs_and_metric_values:
    alert_conf = alert_conf_and_metric_values[0]
    metric_values = alert_conf_and_metric_values[1]
    # save metric value for time window 0
    notification_metric_value_0 = ''
    notification_metric_value_1 = ''
    if metric_values[0] is not None:
        notification_metric_value_0 = str(metric_values[0])
        uri = TEST_ENV.uxpc_base_uri() + str(
            cfg.routes['save-metric-value']) + \
              '?timeWindow=timeWindow0&value=' + str(metric_values[0])
        r = requests.post(uri, json=alert_conf, timeout=TIME_OUT)
    else:
        notification_metric_value_0 = 'null'
    if metric_values[1] is not None:
        notification_metric_value_1 = str(metric_values[1])
        uri = TEST_ENV.uxpc_base_uri() + str(
            cfg.routes['save-metric-value']) + \
              '?timeWindow=timeWindow1&value=' + str(metric_values[1])
        r = requests.post(uri, json=alert_conf, timeout=TIME_OUT)
    else:
        notification_metric_value_1 = 'null'
    #post notification
    if NOTIFICATIONS:
        uri = TEST_ENV.uxpc_base_uri() + str(cfg.routes['notify']) + \
        '?timeWindow0Value=' + notification_metric_value_0 + \
        '&timeWindow1Value=' + notification_metric_value_1
        r = requests.post(uri, json=alert_conf, timeout=TIME_OUT)
        if r.status_code != 200 and r.status_code != 201:
            problems.append((r.status_code, uri, alert_conf))


print('\n-----------------Troubleshooting-----------------------')
for idx, problem in enumerate(problems):
    print('PROBLEM ' + str(idx + 1) + '/' + str(len(problems)) + ' (error code: ' + str(problem[0]) + '):')
    print('ParamsId'+str(problem[2]['alertESParametersId']))
    print('Alert '+str(problem[2]['alertId']))
    #how do we find the associated AlertESParameters with the information which might be causing the problem?
    problematic_alert_configuration = problem[2]
    problematic_alert_es_parameters_id = problematic_alert_configuration['alertESParametersId']
    problematic_alert_es_parameters = [d for d in alert_es_parameters_array if d['id'] == problematic_alert_es_parameters_id][0]
    project_id = problematic_alert_es_parameters['projectId']
    segment_id = problematic_alert_es_parameters['segmentId']
    device_id = problematic_alert_es_parameters['deviceId']
    #verify if extracted ids exist in the test environment
    if TEST_ENV == env.Env.NEXT2:
        pp_base = cfg.next2_config['pp']
    elif TEST_ENV == env.Env.STAGING:
        pp_base = cfg.staging_config['pp']
    elif TEST_ENV == env.Env.LOCAL:
        pp_base = cfg.local_config['pp']
    elif TEST_ENV == env.Env.PRODUCTION:
        pp_base = cfg.production_config['pp']

    #is the projectId ok?
    pp_uri = pp_base + '/projects/' + str(project_id)
    r = requests.get(pp_uri,timeout=TIME_OUT)
    json_data = json.loads(r.text)
    if r.status_code == 200:
        print('Project '+str(project_id)+': '+json_data['name'])
    else:
        print('Problem with projectId when reaching '+pp_uri)

    #is the goalId ok?
    if 'goalId' in problematic_alert_es_parameters:
        metric_name = str(problematic_alert_es_parameters['metric'])
        if metric_name.lower().startswith('conversion'):
            print('Metric name: '+metric_name)
            goal_id = problematic_alert_es_parameters['goalId']
            pp_uri = pp_base + '/projects/' + str(project_id) + '/goals/' + str(goal_id)
            r = requests.get(pp_uri,timeout=TIME_OUT)
            json_data = json.loads(r.text)
            if r.status_code == 200:
                print('Goal ' + str(goal_id) + ': ' + json_data['name'])
            elif goal_id != -1:
                print('Problem with goalId when reaching ' + pp_uri)
            else:
                print('Unidentified problem')
        else:
            print('Metric '+metric_name+' should not have goalId')

    #is the aliasId ok?
    if 'aliasId' in problematic_alert_es_parameters:
        alias_id = problematic_alert_es_parameters['aliasId']
        pp_uri = pp_base + '/pages/' + str(alias_id)
        r = requests.get(pp_uri,timeout=TIME_OUT)
        json_data = json.loads(r.text)
        if r.status_code == 200 and json_data['projectId'] == project_id:
            print('Alias ' + str(alias_id) + ': ' + json_data['name'])
        else:
            print('Problem with aliasId when reaching ' + pp_uri)

    #is the zoneId ok?
    if 'zoneId' in problematic_alert_es_parameters:
        zone_id = problematic_alert_es_parameters['zoneId']
        pp_uri = pp_base + '/zones/' + str(zone_id)
        r = requests.get(pp_uri,timeout=TIME_OUT)
        json_data = json.loads(r.text)
        if r.status_code == 200:
            print('Zone ' + str(zone_id) + ': ' + json_data['name'])
        else:
            print('Problem with zoneId when reaching ' + pp_uri)
    if TEST_ENV == env.Env.LOCAL:
        print('NOTE: update application.conf with '+str(INPUT_ENV).split('.')[1] +' information.')
    print('\t' + "curl --request POST --url '" + problem[1] + "' --header 'content-type: application/json' --data '" + str(
        problem[2]).replace("\'", "\"") + "' -i")
    print('***')
print('-------------------------------------------------------')
