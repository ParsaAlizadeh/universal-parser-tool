from upt.utils import Utils, Driver, By 
from upt.utils.loginmanager import LoginManager

from selenium.webdriver.common.keys import Keys

import getpass
import re, time
import logging


logger = logging.getLogger("atcoder")


class Parser:
    def parse(self, args: list):
        if args[0] == "init":
            return self.initialize()

        self.driver = Driver()
        
        if "-l" in args:
            self.login()
            args.remove("-l")

        url = f"https://atcoder.jp/contests/{args[0]}/tasks/{args[0]}_{args[1]}"
        self.driver.get(url)
        Utils.wait_until(self.driver, By.CSS_SELECTOR, "pre")

        pattern = re.compile(r"pre\-sample\d")
        elements = self.driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and len(elem.text) > 0:
                sample.append(elem.text)

        result = Utils.even_odd(sample)
        Utils.write_samples(result)

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
        Utils.wait_until(self.driver, By.ID, "username")

        user_box = self.driver.find_element_by_id("username")
        user_box.send_keys(user)
        pass_box = self.driver.find_element_by_id("password")
        pass_box.send_keys(pwd)

        user_box.send_keys(Keys.ENTER)
        Utils.wait_until(self.driver, By.CSS_SELECTOR, ".alert")
        alert = self.driver.find_element_by_css_selector(".alert")
        
        assert "Welcome" in alert.text, "Login failed"
        logger.info("Logged in")

