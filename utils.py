from enum import Enum

import serviceConfig as cfg


class Env(Enum):
    NEXT2 = str(cfg.next2_config['host']) + ':' + str(cfg.next2_config['port'])
    STAGING = str(cfg.staging_config['host']) + ':' + str(cfg.staging_config['port'])
    PRODUCTION = str(cfg.production_config['host']) + ':' + str(cfg.production_config['port'])
    LOCAL = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port'])

    def base_uri(self):
        return self.value