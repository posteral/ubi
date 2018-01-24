from enum import Enum

import serviceConfig as cfg


class Env(Enum):
    STAGING = str(cfg.staging_config['host']) + ':' + str(cfg.staging_config['port'])
    PRODUCTION = ''
    LOCAL = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port'])

    def base_uri(self):
        return self.value
