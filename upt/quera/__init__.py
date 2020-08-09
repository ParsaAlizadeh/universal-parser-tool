import argparse
import logging
import sys

from ..util import Util, Driver
from ..util.loginmanager import LoginManager

logger = logging.getLogger("quera")


class Parser:
    usage = "upt quera [-h] [-l] [-u URL] [--init] ..."
    TYPE = {"con": "contest",
            "oly": "olympiad",
            "uni": "university"}

    def __init__(self):
        self.driver = None

    def parse(self, args: list):
        argparser = argparse.ArgumentParser(prog="upt quera",
                                            usage=Parser.usage)
        argparser.add_argument("task",
                               nargs="*",
                               help=argparse.SUPPRESS)
        argparser.add_argument("-l",
                               "--login",
                               help="Login to atcoder before parse the problem",
                               action="store_true")
        argparser.add_argument("-u",
                               "--url",
                               nargs=1,
                               help="Task custom url", )
        argparser.add_argument("--init",
                               nargs=0,
                               help="Initialize login data",
                               action=self.init_action())

        args = argparser.parse_args(args)

        if not args.url:
            problem_type = args.task[0]
            assert problem_type in Parser.TYPE, f"Type \"{problem_type}\" not supported"

            problem_type = Parser.TYPE.get(problem_type)
            problem_code = int(args.task[1])
            url = f"http://quera.ir/problemset/{problem_type}/{problem_code}/"
        else:
            url = args.url[0]

        self.driver = Driver(nostrategy=False)
        if args.login:
            self.login()
        self.driver.get(url)

        sample = Util.get_sample(self.driver)
        result = Util.even_odd(sample)
        Util.write_samples(result)

    def init_action(self):
        class MyAction(argparse.Action):
            def __init__(self, option_strings, dest, **kwargs):
                super(MyAction, self).__init__(option_strings, dest, **kwargs)

            def __call__(self, parser, namespace, values, option_string=None):
                login = LoginManager("quera")
                login.get_auth()
                login.write()
                sys.exit()

        return MyAction

    def login(self):
        logger.info("Trying to login")
        login = LoginManager("quera")
        user, pwd = login.read_auth()

        url = "https://quera.ir/accounts/login"
        self.driver.get(url)

        user_box = self.driver.find_element_by_name("login")
        user_box.send_keys(user)
        pass_box = self.driver.find_element_by_name("password")
        pass_box.send_keys(pwd)

        submit_btn = self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/form/div[3]")
        submit_btn.click()

        assert "dashboard" in self.driver.current_url, "Login failed"
        logger.info("Logged in")
