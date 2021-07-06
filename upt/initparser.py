from .baseparser import BaseParser
from .configmanager import ConfigManager


class InitParser(BaseParser):
    @property
    def description(self):
        return 'Initialize configs'

    @property
    def aliases(self):
        return ('init',)

    def __init__(self, alias=None):
        super().__init__(alias)
        self._confman = ConfigManager()
        for option in self._confman.options:
            self._argparser.add_argument(
                f'--{option.name}',
                default=None,
                help=option.help
            )

    def parse(self, args):
        to_prompt = True
        for option in self._confman.options:
            value = getattr(args, option.name)
            if value is None:
                continue
            to_prompt = False
            self._confman.set_option(option.name, value)

        if to_prompt:
            self.prompt()

        self._confman.save_file()

    def prompt(self):
        for option in self._confman.options:
            value = input(f'== {option.help} (default: {option.default}): ')
            value = value or option.default
            self._confman.set_option(option.name, value)
