import logging
import operator
import os
from functools import reduce

import yaml


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


class ConfigClass:
    """
    Application-wide config object
    """
    _config = {
        'env': os.getenv('ENV', 'dev'),
        'soap_api': {
            'user_name': os.getenv('SOAP_USER', ''),
            'user_token': os.getenv('SOAP_TOKEN', ''),
            'endpoint': os.getenv('SOAP_ENDPOINT', ''),
        },
        'server': {
            'host': os.getenv('HOST', '127.0.0.1'),
            'port': int(os.getenv('PORT', '5000')),
            'log_level': os.getenv('LOG_LEVEL', 'info'),
            'timeout_keep_alive': 0,
        },
        'log_level': 'info',
    }

    def merge(self, cfg):
        self._config = {**self._config, **cfg}

    def dump(self, logger):
        logger.debug('config: %s', yaml.dump(self._config, indent=2))

    def key(self, k):
        if isinstance(k, list):
            return get_by_path(self._config, k)
        return self._config.get(k, False)

    def set(self, k, v):
        if isinstance(k, list):
            set_by_path(self._config, k, v)
        else:
            self._config[k] = v


config = ConfigClass()
