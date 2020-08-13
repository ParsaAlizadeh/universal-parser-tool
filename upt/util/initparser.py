import argparse
import logging
import os
from configparser import ConfigParser

from . import CONFIG_PATH

logger = logging.getLogger("init")


class InitParser:
    usage = "upt init [-h] [path]"
    config_parser = None

    def __init__(self):
        if self.config_parser is None:
            self.config_parser = ConfigParser()
            self.config_parser.read(CONFIG_PATH)

    def parse(self, args: list):
        argparser = argparse.ArgumentParser(prog="upt init",
                                            usage=InitParser.usage)
        argparser.add_argument("path",
                               nargs="?",
                               default=None,
                               help="New root path")
        args = argparser.parse_args(args)

        if args.path is None:
            args.path = input("== Set Root Path (e.g. ~/cf/): ")

        args.path = os.path.expanduser(args.path)
        if args.path[-1] == "/":
            args.path = args.path[:-1]

        if not self.config_parser.has_section("upt"):
            self.config_parser.add_section("upt")
        self.config_parser["upt"]["root"] = args.path

        with open(CONFIG_PATH, "w") as file:
            self.config_parser.write(file)

        logger.info("Root path changed to " + args.path)

    def get_path(self, path, makedir=False):
        assert self.config_parser.has_section("upt"), "Run \"upt init\" first"
        assert self.config_parser["upt"]["root"] is not None, "Run \"upt init\" first"

        path = "/" if path is None else path
        path = self.config_parser["upt"]["root"] + path

        if makedir:
            os.system("mkdir -p " + path)

        return path
