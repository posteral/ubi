import requests

import serviceConfig as cfg


def fetchAlertConfigs(env):
    # build URI from configuration file
    uri = env.uxpc_base_uri() + str(cfg.routes['fetch-alert-configs'])
    print(uri)
    r = requests.post(uri, timeout=10)
    return r
