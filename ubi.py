import requests
import serviceConfig as cfg


uri = str(cfg.staging_config['host'])+':'+str(cfg.staging_config['port'])+str(cfg.routes['fetch-alert-configs'])
print(uri)
r = requests.post(uri, data={'number': 12524, 'type': 'issue', 'action': 'show'})
print(r.status_code, r.reason)
print(cfg.staging_config)
print(r.json())