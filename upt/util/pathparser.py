from configparser import ConfigParser
from os.path import expanduser
from . import CONFIG

import os
import logging


logger = logging.getLogger("path")


class PathParser:
    configparser = None

    def __init__(self):
        if self.configparser is None:
            self.configparser = ConfigParser()
            self.configparser.read(CONFIG)
    
    def parse(self, args :list):
        path = args[0] if len(args) > 0 else None
        if path is None:
            path = input("==== Set Root Path (e.g. ~/cf/contest): ")
        path = expanduser(path)
        if path[-1] == "/":
            path = path[:-1]
        
        if not self.configparser.has_section("upt"):
            self.configparser.add_section("upt")
        self.configparser["upt"]["root"] = path
        
        with open(CONFIG, "w") as file:
            self.configparser.write(file)

        logger.info("Root path changed to " + path)
    
    def get_path(self, path:str = None, makedir:bool = False) -> str:
        assert self.configparser.has_section("upt"), "Run \"upt init\" first"
        assert self.configparser["upt"]["root"] is not None, "Run \"upt init\" first"

        path = "/" if path is None else path
        path = self.configparser["upt"]["root"] + path

        if makedir:
            os.system("mkdir -p " + path)

        return path

