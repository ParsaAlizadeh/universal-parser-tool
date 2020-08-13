import logging
import argparse
import sys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from .driver import Driver
from .initparser import InitParser
from .loginmanager import LoginManager
from . import sample_common

logger = logging.getLogger("parser")


def wait_until(driver, by, name):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((by, name)))
    driver.execute_script("window.stop();")


class TemplateParser:
    name = "<parser>"
    usage = "upt <parser> <commands>"

    def __init__(self, login_options=None, driver_options=None):
        if driver_options is None:
            driver_options = {}
        self.argparser = argparse.ArgumentParser(prog=self.__class__.name,
                                                 usage=self.__class__.usage)

        if login_options:
            self.argparser.add_argument("--init",
                                        nargs=0,
                                        action=self.__init_action(),
                                        help="Initialize data",)
            self.argparser.add_argument("-l",
                                        "--login",
                                        action="store_true",
                                        help="Login before parse",)
        self.argparser.add_argument("-i",
                                    "--inplace",
                                    action="store_true",
                                    help="Create Tests inplace",)
        self.argparser.add_argument("-u",
                                    "--url",
                                    nargs=1,
                                    help="Custom task url",)
        self.argparser.add_argument("task",
                                    nargs="*",
                                    help=argparse.SUPPRESS)
        self.driver = None
        self.driver_options = driver_options
        self.login_options = login_options

    def __init_action(self):
        class MyAction(argparse.Action):
            def __init__(obj, option_strings, dest, **kwargs):
                super(MyAction, obj).__init__(option_strings, dest, **kwargs)

            def __call__(obj, parser, namespace, values, option_string=None):
                self.initialize()
                sys.exit()
        return MyAction

    def initialize(self):
        login = LoginManager(self.__class__.name)
        login.get_auth()
        login.write()

    def url_finder(self, *task):
        raise Exception("No url_finder function for this parser")

    def placer(self, *task):
        raise Exception("No placer function for this parser")

    def sampler(self, elements):
        return sample_common.Sampler.even_odd(elements)

    def login(self, url, username, password, submit, checker):
        logger.info("Trying to login")
        login = LoginManager(self.__class__.name)
        user, pwd = login.read_auth()

        self.driver.get(url)
        if not self.driver_options.get("nostrategy") is False:
            wait_until(self.driver, *username)

        user_box = self.driver.find_element(*username)
        user_box.send_keys(user)
        pass_box = self.driver.find_element(*password)
        pass_box.send_keys(pwd)

        submit_btn = self.driver.find_element(*submit)
        submit_btn.click()

        checker(self.driver)

    def parse(self, args):
        args = self.argparser.parse_args(args)

        url = args.url[0] if args.url else self.url_finder(*args.task)
        path = "./" if args.inplace or args.url else InitParser().get_path(self.placer(*args.task), makedir=True)

        self.driver = Driver(**self.driver_options)
        if self.login_options and args.login:
            self.login(**self.login_options)
            logger.info("Logged in")

        self.driver.get(url)
        if not self.driver_options.get("nostrategy") is False:
            wait_until(self.driver, By.CSS_SELECTOR, "pre")
        elements = self.driver.find_elements_by_css_selector("pre")

        samples = self.sampler(elements)
        sample_common.write_samples(samples, path)
