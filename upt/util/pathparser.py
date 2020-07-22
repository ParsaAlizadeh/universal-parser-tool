import argparse
import logging
import os
from configparser import ConfigParser
from os.path import expanduser

from . import CONFIG

logger = logging.getLogger("path")


class PathParser:
    usage = "upt init [-h] <path>"
    configparser = None

    def __init__(self):
        if self.configparser is None:
            self.configparser = ConfigParser()
            self.configparser.read(CONFIG)

    def parse(self, args: list):
        argparser = argparse.ArgumentParser(prog="upt init",
                                            usage=PathParser.usage)
        argparser.add_argument(
            "path",
            nargs="?",
            default=None,
            help="New root path")
        args = argparser.parse_args(args)

        if args.path is None:
            args.path = input("== Set Root Path (e.g. ~/cf/contest): ")

        args.path = expanduser(args.path)
        if args.path[-1] == "/":
            args.path = args.path[:-1]

        if not self.configparser.has_section("upt"):
            self.configparser.add_section("upt")
        self.configparser["upt"]["root"] = args.path

        with open(CONFIG, "w") as file:
            self.configparser.write(file)

        logger.info("Root path changed to " + args.path)

    def get_path(self, path: str = None, makedir: bool = False) -> str:
        assert self.configparser.has_section("upt"), "Run \"upt init\" first"
        assert self.configparser["upt"]["root"] is not None, "Run \"upt init\" first"

        path = "/" if path is None else path
        path = self.configparser["upt"]["root"] + path

        if makedir:
            os.system("mkdir -p " + path)

        return path
