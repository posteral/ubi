from enum import Enum

import serviceConfig as cfg


class Env(Enum):
    NEXT2 = str(cfg.next2_config['host']) + ':' + str(cfg.next2_config['port'])
    STAGING = str(cfg.staging_config['host']) + ':' + str(cfg.staging_config['port'])
    PRODUCTION = str(cfg.production_config['host']) + ':' + str(cfg.production_config['port'])
    LOCAL = str(cfg.local_config['host']) + ':' + str(cfg.local_config['port'])

    def base_uri(self):
        return self.value

    def pp_base_uri(self):
        return self.__config_selector('pp')

    def pages_comparator_base_uri(self):
        return self.__config_selector('pcomp')

    def mappings_file(self):
        if self == Env.NEXT2:
            return 'stats/next2_mappings_per_project.txt'
        elif self == Env.STAGING:
            return 'stats/staging_mappings_per_project.txt'
        elif self == Env.PRODUCTION:
            return 'stats/production_mappings_per_project.txt'
        else:
            return 'stats/staging_mappings_per_project.txt'

    def __config_selector(self, key):
        if self == Env.NEXT2:
            return cfg.next2_config[key]
        elif self == Env.STAGING:
            return cfg.staging_config[key]
        elif self == Env.PRODUCTION:
            return cfg.production_config[key]
        else:
            return cfg.local_config[key]


