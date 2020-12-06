import argparse
import logging
import os
from configparser import ConfigParser

from . import CONFIG_PATH, CONFIG_FILE

logger = logging.getLogger("init")


class NotInitialized(Exception):
    pass


def prompt(args):
    args.root = input("== Set root path (default=~/codeforces/): ")
    args.root = args.root if args.root else "~/codeforces/"
    args.input = input("== Set input file format (default={i}.in): ")
    args.input = args.input if args.input else "{i}.in"
    args.output = input("== Set output file format (default={i}.out): ")
    args.output = args.output if args.output else "{i}.out"


class InitParser:
    usage = "[-h] [--root ROOT] [--input INPUT] [--output OUTPUT]"
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
        argparser = argparse.ArgumentParser(prog=f"upt {self.alias}",
                                            usage=f"upt {self.alias} {self.__class__.usage}")
        argparser.add_argument("--root",
                               default=None,
                               help="root path")
        argparser.add_argument("--input",
                               default=None,
                               help="input file format")
        argparser.add_argument("--output",
                               default=None,
                               help="output file format")
        args = argparser.parse_args(args)

        if (not (args.root or args.input or args.output)
                or any(not self.exists(i) for i in ("root", "input", "output"))):
            prompt(args)

        if args.root:
            args.root = os.path.expanduser(args.root)
            self["root"] = args.root

        if args.input:
            self["input"] = args.input

        if args.output:
            self["output"] = args.output

        self.write()

    def exists(self, item):
        return item in self.config_parser["upt"]

    def write(self):
        logger.info("Writing configurations")
        with open(CONFIG_FILE, "w") as file:
            self.config_parser.write(file)

    def __getitem__(self, item):
        if item not in self.config_parser["upt"]:
            logger.error(f"Not initialized {item}")
            raise NotInitialized()
        return self.config_parser["upt"][item]

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
