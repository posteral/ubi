import requests
import dbconfig as cfg

r = requests.post("http://bugs.python.org", data={'number': 12524, 'type': 'issue', 'action': 'show'})
print(r.status_code, r.reason)
print(cfg.uxpc_alerts_db_staging_config)


#first we need to find a way to have a configuration file