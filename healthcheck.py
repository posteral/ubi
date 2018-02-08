# This script executes heathcheck queries on a set of services
from env import Env
import json

import requests

TEST_ENV = Env.PRODUCTION

services_being_tested = dict()
services_being_tested['pages-comparator'] = TEST_ENV.pages_comparator_base_uri()


for service_name, base_uri in services_being_tested.items():
    uri = base_uri + '/healthcheck'
    response = requests.get(uri)
    if response.status_code != 200: #failure
        print(service_name+': Unhealthy')
    else:
        json = json.loads(response.text)
        print(json)