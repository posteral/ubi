import requests

from joblib import Parallel, delayed
import multiprocessing

local_base_uri ='http://localhost:9005'
staging_base_uri ='http://hpg-pages-comparator-staging.csq.io:8080'
production_base_uri ='http://hpg-pages-comparator.csq.io:8080'


uri = staging_base_uri + '/pages-comparator/v1/projects/88/version'


def execute_request():
    print(uri)
    response = requests.get(uri)
    print(response.text)


num_cores = multiprocessing.cpu_count()

print(num_cores)

results = Parallel(n_jobs=num_cores)(delayed(execute_request)() for i in range(10000))


#for x in range(1000):
#    response = requests.get(uri)
#    print(response.text)

