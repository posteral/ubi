# This script executes heathcheck queries on a set of services
from env import Env
import json

import requests

TEST_ENV = Env.PRODUCTION

services_being_tested = dict()

services_being_tested['pages-comparator'] = TEST_ENV.pages_comparator_base_uri()
services_being_tested['ws-uxpc-alerts'] = TEST_ENV.uxpc_base_uri()

for service_name, base_uri in services_being_tested.items():
    uri = base_uri + '/healthcheck'
    response = requests.get(uri)
    if response.status_code != 200: #failure
        print(service_name+': Unhealthy')
    else:
        json_response = json.loads(response.text)
        status = json_response['state']
        if status:
            print(service_name + ': Unhealthy')
        else:
            print(service_name + ': Healthy')