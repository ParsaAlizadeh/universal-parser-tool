import argparse
import datetime
import http
import logging
import time

import requests
import selenium
from bs4 import BeautifulSoup

from . import sampler
from .driver import Driver
from .initparser import InitParser
from .session import Session

logger = logging.getLogger("parser")


class LoginFailedError(Exception):
    pass


class NotImplemented(Exception):
    pass


class BaseParser:
    name = "<parser>"
    usage = "upt <parser> <commands>"

    def __init__(self, login_page=False):
        self.argparser = argparse.ArgumentParser(prog=self.__class__.name,
                                                 usage=self.__class__.usage)

        if login_page:
            self.argparser.add_argument("-l",
                                        "--login",
                                        action="store_true",
                                        help="Login before parse", )
            self.login_page = login_page
        self.argparser.add_argument("-i",
                                    "--inplace",
                                    action="store_true",
                                    help="Create Tests inplace", )
        self.argparser.add_argument("-u",
                                    "--url",
                                    nargs=1,
                                    help="Custom task url", )
        self.argparser.add_argument("task",
                                    nargs="*",
                                    help=argparse.SUPPRESS)
        self.session = Session()

    def __del__(self):
        self.session.save_cookiejar()

    def url_finder(self, *task):
        raise NotImplemented("No url_finder function for this parser")

    def placer(self, *task):
        raise NotImplemented("No placer function for this parser")

    def sampler(self, soup: BeautifulSoup):
        raise NotImplemented("No sampler function for this parser")

    def login(self):
        with Driver() as driver:
            url = self.login_page
            logger.info('Opening the URL via WebDriver: %s', url)
            logger.info('Please do the followings:\n    1. login in the GUI browser\n    2. close the GUI browser')
            driver.get(url)
            cookies = []
            try:
                while driver.current_url:
                    cookies = driver.get_cookies()
                    time.sleep(0.1)
            except:
                pass

        logger.info('Copying cookies via WebDriver...')
        for c in cookies:
            logger.debug('set cookie: %s', c['name'])
            morsel: http.cookies.Morsel = http.cookies.Morsel()
            morsel.set(c['name'], c['value'], c['value'])
            morsel.update({key: value for key, value in c.items() if morsel.isReservedKey(key)})
            if not morsel['expires']:
                expires = datetime.datetime.now(datetime.timezone.utc).astimezone() + datetime.timedelta(days=180)
                morsel.update({'expires': expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT')})  # RFC2109 format
            cookie = requests.cookies.morsel_to_cookie(morsel)
            self.session.cookies.set_cookie(cookie)

    def parse(self, args):
        args = self.argparser.parse_args(args)

        if args.login and self.login_page:
            return self.login()

        try:
            url = args.url[0] if args.url else self.url_finder(*args.task)
            path = "./" if args.inplace or args.url else InitParser().get_path(self.placer(*args.task), makedir=True)
        except TypeError:
            logger.error("Something wrong with given task")
            raise

        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        samples = self.sampler(soup)
        sampler.write_samples(samples, path)
