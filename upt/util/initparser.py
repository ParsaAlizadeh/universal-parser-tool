import argparse
import logging
import os
from configparser import ConfigParser

from . import CONFIG_PATH, CONFIG_FILE

logger = logging.getLogger("init")


class NotInitialized(Exception):
    pass


class InitParser:
    config_parser = None

    def __init__(self, alias):
        self.alias = alias
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        if self.config_parser is None:
            self.config_parser = ConfigParser()
            self.config_parser.read(CONFIG_FILE)
        if not self.config_parser.has_section("upt"):
            self.config_parser.add_section("upt")

    def parse(self, args):
        argparser = argparse.ArgumentParser(
            prog=f"upt {self.alias}",
            description='Initialize configs'
        )
        argparser.add_argument(
            "--root",
            default=None,
            help="root path"
        )
        argparser.add_argument(
            "--input",
            default=None,
            help="input file format"
        )
        argparser.add_argument(
            "--output",
            default=None,
            help="output file format"
        )
        args = argparser.parse_args(args)

        if any((args.root, args.input, args.output)):
            args.root = args.root or self.get('root')
            args.input = args.input or self.get('input')
            args.output = args.output or self.get('output')

        if not all((args.root, args.input, args.output)):
            self.prompt(args)

        args.root = os.path.expanduser(args.root)
        self["root"] = args.root
        self["input"] = args.input
        self["output"] = args.output
        self.write()

    @staticmethod
    def prompt(args, defaults=None):
        if defaults is None:
            defaults = {
                'root': '~/codeforces',
                'input': '{i}.in',
                'output': '{i}.out',
            }
        if args.root is None:
            args.root = input(f"== Set root path (default: {defaults['root']}): ")
            args.root = args.root if args.root else defaults['root']
        if args.input is None:
            args.input = input(f"== Set input file format (default: {defaults['input']}): ")
            args.input = args.input if args.input else defaults['input']
        if args.output is None:
            args.output = input(f"== Set output file format (default: {defaults['output']}): ")
            args.output = args.output if args.output else defaults['output']

    def write(self):
        logger.info("Writing configurations")
        with open(CONFIG_FILE, "w") as file:
            self.config_parser.write(file)

    def exists(self, item):
        return item in self.config_parser["upt"]

    def __getitem__(self, item):
        if item not in self.config_parser["upt"]:
            logger.error("Not initialized %s", item)
            raise NotInitialized()
        return self.config_parser["upt"][item]

    def get(self, item, default=None):
        return self[item] if self.exists(item) else default

    def __setitem__(self, key, value):
        self.config_parser["upt"][key] = value
        return value

    def get_path(self, path="./", makedir=False):
        path = os.path.join(self["root"], path)
        if makedir:
            try:
                os.makedirs(path)
            except OSError:
                logger.warning("Problem path created before")
        return path

    def get_input(self, index):
        return self["input"].format(i=index)

    def get_output(self, index):
        return self["output"].format(i=index)
