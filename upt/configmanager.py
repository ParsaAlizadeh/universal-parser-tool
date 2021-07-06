import logging
import os
from configparser import ConfigParser
from typing import List, NamedTuple

from .constants import CONFIG_FILE, CONFIG_PATH

logger = logging.getLogger('config')


class ConfigOption(NamedTuple):
    name: str
    default: str
    help: str


class _SingletonConfig(type):
    obj = None

    def __call__(cls, *args, **kwargs):
        if _SingletonConfig.obj is None:
            _SingletonConfig.obj = super().__call__(*args, **kwargs)
        return _SingletonConfig.obj


class ConfigManager(metaclass=_SingletonConfig):
    options: List[ConfigOption] = [
        ConfigOption(
            name='root',
            default='~/codeforces',
            help='root path'
        ),
        ConfigOption(
            name='input',
            default='{i}.in',
            help='input filename format'
        ),
        ConfigOption(
            name='output',
            default='{i}.out',
            help='output filename format'
        ),
    ]

    def __init__(self):
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        self._config_parser = ConfigParser()
        self._config_parser.read(CONFIG_FILE) # Ignore if file not exists
        if not self._config_parser.has_section('upt'):
            self._config_parser.add_section('upt')
        self._init_defaults()

    def save_file(self):
        logger.info('Saving configs')
        with open(CONFIG_FILE, 'w') as file:
            self._config_parser.write(file)

    def get_option(self, option):
        return self._config_parser.get('upt', option, fallback=None)

    def set_option(self, option, value):
        return self._config_parser.set('upt', option, value)

    def _init_defaults(self):
        for option in self.options:
            if self.get_option(option.name) is None:
                self.set_option(option.name, option.default)

    def __getattr__(self, name):
        for option in self.options:
            if name == option.name:
                return self.get_option(name)
        raise AttributeError

    def __setattr__(self, name, value):
        for option in self.options:
            if name == option.name:
                return self.set_option(name, value)
        return super().__setattr__(name, value)

    def path_from_root(self, path="./", makedir=False):
        root = os.path.expanduser(self.root)
        path = os.path.join(root, path)
        if makedir:
            os.makedirs(path, exist_ok=True)
        return path

    def input_path(self, index):
        return self.input.format(i=index)

    def output_path(self, index):
        return self.output.format(i=index)
