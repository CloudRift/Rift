"""
This module handles the loading of configuration settings for the application.
The module first loads default config values and then attempts to read
settings from a config file.
A RiftConfiguration object is created once and is provided by reference to
other modules through the get_config module.
"""

from ConfigParser import ConfigParser
import os.path

_CONFIG_FILE = '/opt/cloudrift/etc/rift/rift.conf'

_CFG_DEFAULTS = {
    'logging': {
        'log_level': 'DEBUG'
    },
    'mongodb': {
        'server': 'localhost:27017',
        'database': 'rift'
    },
    'celery': {
        'broker_url': 'amqp://guest@localhost//',
        'celeryd_concurrency': 2,
        'celery_task_serializer': "json",
        'celeryd_hijack_root_logger': False

    }
}


class ConfigSection(object):
    """
    Class for a configuration section that allows for dynamic settings of
    options as attributes
    """
    def add_option(self, option, value):
        self.__setattr__(option, value)


class RiftConfiguration(object):
    """
    Class that holds all configuration settings as attributes.
    The class allows the loading of default config values from a dictionary
    and for loading of config values from a stdlib ConfigParser object.
    """
    def __init__(self, default_cfg):
        self.load_defaults(default_cfg)

    def load_defaults(self, default_cfg):
        """
        Set attributes from ConfigSection objects created from a dictionary
        of default config values
        """
        for section_name in default_cfg:
            section = ConfigSection()
            for option in default_cfg[section_name]:
                section.add_option(option, default_cfg[section_name][option])
            self.__setattr__(section_name, section)

    def load_config(self, cfg_parser):
        """
        Set attributes from ConfigSection objects created from a dictionary
        of default config values
        """
        for section_name in cfg_parser.sections():
            section = ConfigSection()
            for option in cfg_parser.options(section_name):
                section.add_option(option, cfg_parser.get(section_name,
                                                          option))
            self.__setattr__(section_name, section)


_cfg = RiftConfiguration(_CFG_DEFAULTS)


def load_config(config_file=_CONFIG_FILE):
    cfg_parser = ConfigParser()
    if not os.path.isfile(config_file):
        raise Exception(
            'configuration file not found: {0}'.format(config_file))
    cfg_parser.read(config_file)
    _cfg.load_config(cfg_parser)


def get_config():
    config = _CONFIG_FILE
    if os.path.exists('./etc/rift/rift.conf'):
        config = os.path.abspath('./etc/rift/rift.conf')

    load_config(config_file=config)
    return _cfg
