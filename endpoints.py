import requests

import serviceConfig as cfg


def fetchAlertConfigs(env) :
    # build URI from configuration file
    uri = env + str(cfg.routes['fetch-alert-configs'])
    r = requests.post(uri, timeout=10)
    return r