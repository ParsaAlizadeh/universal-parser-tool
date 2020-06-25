from configparser import ConfigParser
from os.path import expanduser
import getpass
import logging

CONFIGPATH = expanduser("~/.upt.ini")

class LoginManager:
    configparser = None

    def __init__(self, name):
        if self.configparser is None:
            self.configparser = ConfigParser()
            self.configparser.read(CONFIGPATH)
        self.name = name

    def get_auth(self):
        print("===================================")
        print(f"== Login for {self.name} ==")
        user = input("Username: ")
        pwd = getpass.getpass("Password: ")
        print("===================================")
        
        if not self.configparser.has_section(self.name):
            self.configparser.add_section(self.name)

        self.configparser[self.name]["username"] = user
        self.configparser[self.name]["password"] = pwd

    def read_auth(self):
        assert self.configparser.has_section(self.name), f"no login data for {self.name}"
        user = self.configparser[self.name]["username"]
        pwd = self.configparser[self.name]["password"]
        return (user, pwd)

    def write(self):
        with open(CONFIGPATH, "w") as file:
            self.configparser.write(file)

