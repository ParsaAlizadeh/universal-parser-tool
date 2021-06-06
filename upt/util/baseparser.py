import argparse
import datetime
import http
import logging
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchWindowException

from . import sampler
from .driver import Driver
from .initparser import InitParser
from .session import Session

logger = logging.getLogger("base")


class LoginFailedError(Exception):
    pass


class NotRecognizedProblem(Exception):
    pass


class BaseParser:
    description = 'Base class for parsers'
    url_regex = re.compile(r"^http[s]?://")
    login_page = None

    def __init__(self, alias):
        self.alias = alias
        self.argparser = argparse.ArgumentParser(
            prog=f'upt {self.alias}',
            description=self.description
        )

        if self.login_page:
            self.argparser.add_argument(
                "-l", "--login",
                action="store_true",
                help="login to service",
            )
        self.argparser.add_argument(
            "-i", "--inplace",
            action="store_true",
            help="create tests inplace",
        )
        self.argparser.add_argument(
            "task",
            nargs="*",
            help='formatted taskname or task url'
        )
        self.session = Session()

    def __del__(self):
        self.session.save_cookiejar()

    def url_finder(self, *task):
        raise NotImplementedError("No url_finder function for this parser")

    def placer(self, *task):
        raise NotImplementedError("No placer function for this parser")

    def sampler(self, soup: BeautifulSoup):
        raise NotImplementedError("No sampler function for this parser")

    def login(self):
        with Driver() as driver:
            url = self.login_page
            logger.info('Opening the URL via WebDriver: %s', url)
            logger.info(
                'Please do the followings:\n'
                '    1. login in the GUI browser\n'
                '    2. close the GUI browser'
            )
            driver.get(url)
            cookies = []
            try:
                while driver.current_url:
                    cookies = driver.get_cookies()
                    time.sleep(0.1)
            except NoSuchWindowException:
                pass
            except Exception as err:
                logger.warning('Ignore error %s', type(err))

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
            self.login()
            return

        if len(args.task) == 1 and self.url_regex.match(args.task[0]):
            url = args.task[0]
            args.inplace = True
        else:
            try:
                url = self.url_finder(*args.task)
            except NotRecognizedProblem:
                logger.error("Given task not recognized")
                return

        try:
            path = "./" if args.inplace \
                else InitParser(alias=None).get_path(self.placer(*args.task), makedir=True)
        except TypeError:
            logger.error("Something wrong with given task")
            raise

        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        samples = self.sampler(soup)
        if not samples:
            logger.warning("No sample found, make sure you logged in and this url exists")
            return
        sampler.write_samples(samples, path)
