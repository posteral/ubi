from enum import Enum

import serviceConfig as cfg


class Env(Enum):
    NEXT2 = 1
    STAGING = 2
    PRODUCTION = 3
    LOCAL = 4

    def pp_base_uri(self):
        return self.__base_uri('pp')

    def dashboard_base_uri(self):
        return self.__base_uri('dashboard')

    def hpg_base_uri(self):
        return self.__base_uri('hpg')

    def pages_comparator_base_uri(self):
        return self.__base_uri('pcomp')

    def uxpc_base_uri(self):
        return self.__base_uri('uxpc')


    def mappings_file(self):
        if self == Env.NEXT2:
            return 'stats/next2_mappings_per_project.txt'
        elif self == Env.STAGING:
            return 'stats/staging_mappings_per_project.txt'
        elif self == Env.PRODUCTION:
            return 'stats/production_mappings_per_project.txt'
        else:
            return 'stats/staging_mappings_per_project.txt'

    def __base_uri(self, service_name):
        return self.__config_selector(service_name) + ':' + str(self.__config_selector('port'))

    def __config_selector(self, key):
        if self == Env.NEXT2:
            return cfg.next2_config[key]
        elif self == Env.STAGING:
            return cfg.staging_config[key]
        elif self == Env.PRODUCTION:
            return cfg.production_config[key]
        else:
            return cfg.local_config[key]


