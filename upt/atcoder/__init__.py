from ..util import Util, Driver, By 
from ..util.loginmanager import LoginManager
from ..util.pathparser import PathParser

from selenium.webdriver.common.keys import Keys
import argparse

import re
import logging


logger = logging.getLogger("atcoder")


class Parser:
    def parse(self, args: list):
        argparser = argparse.ArgumentParser(prog="upt atcoder",
                                            description="example: upt atcoder agc044 b")
        argparser.add_argument("-l", "--login", help="Login to atcoder before parse the problem", action="store_true")
        argparser.add_argument("-i", "--inplace", help="Create tests inplace instead of root", action="store_true")
        argparser.add_argument("task", nargs="+")
        args = argparser.parse_args(args)

        if args.task == ["init"]:
            return self.initialize()

        assert len(args.task) == 2, "Arguments not correct"

        contest, index = args.task
        url = f"https://atcoder.jp/contests/{contest}/tasks/{contest}_{index}"
        path = "./" if args.inplace else PathParser().get_path(f"/{contest}/{index}", makedir=True)

        self.driver = Driver()
        if args.login:
            self.login()
        self.driver.get(url)
        Util.wait_until(self.driver, By.CSS_SELECTOR, "pre")

        pattern = re.compile(r"pre\-sample\d")
        elements = self.driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and len(elem.text) > 0:
                sample.append(elem.text)

        result = Util.even_odd(sample)
        Util.write_samples(result, path=path)

    def initialize(self):
        login = LoginManager("atcoder")
        login.get_auth()
        login.write()

    def login(self):
        logger.info("Trying to login")
        login = LoginManager("atcoder")
        user, pwd = login.read_auth()
        
        url = "https://atcoder.jp/login"
        self.driver.get(url)
        Util.wait_until(self.driver, By.ID, "username")

        user_box = self.driver.find_element_by_id("username")
        user_box.send_keys(user)
        pass_box = self.driver.find_element_by_id("password")
        pass_box.send_keys(pwd)

        user_box.send_keys(Keys.ENTER)
        Util.wait_until(self.driver, By.CSS_SELECTOR, ".alert")
        alert = self.driver.find_element_by_css_selector(".alert")
        
        assert "Welcome" in alert.text, "Login failed"
        logger.info("Logged in")

