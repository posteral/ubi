import requests

import serviceConfig as cfg


def fetchAlertConfigs(base_uri) :
    # build URI from configuration file
    uri = base_uri + str(cfg.routes['fetch-alert-configs'])
    r = requests.post(uri, timeout=10)
    return r