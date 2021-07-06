import datetime
import http
import logging
import re
import time
from abc import abstractmethod
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from . import sampler
from .baseparser import BaseParser
from .configmanager import ConfigManager
from .driver import get_webdriver
from .session import Session

logger = logging.getLogger("service")


class BadTaskError(Exception):
    pass


class ServiceParser(BaseParser):
    url_regex = re.compile(r"^http[s]?://")

    @property
    @abstractmethod
    def login_page(self) -> Optional[str]:
        ...

    def __init__(self, alias=None):
        super().__init__(alias)
        if self.login_page:
            self._argparser.add_argument(
                "-l", "--login",
                action="store_true",
                help="login to service",
            )
        self._argparser.add_argument(
            "-i", "--inplace",
            action="store_true",
            help="create tests inplace",
        )
        self._argparser.add_argument(
            "task",
            nargs="*",
            help='formatted taskname or task url'
        )
        self._session = Session()

    @abstractmethod
    def url_finder(self, task) -> str:
        ...

    @abstractmethod
    def placer(self, task) -> str:
        ...

    @abstractmethod
    def sampler(self, soup: BeautifulSoup) -> List[List[str]]:
        ...

    def login(self) -> None:
        with get_webdriver() as driver:
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
            except:
                pass

        logger.info('Copying cookies via WebDriver...')
        for c in cookies:
            logger.debug('set cookie: %s', c['name'])
            morsel: http.cookies.Morsel = http.cookies.Morsel()
            morsel.set(c['name'], c['value'], c['value'])
            morsel.update({key: value for key, value in c.items() if morsel.isReservedKey(key)})
            if not morsel['expires']:
                expires = datetime.datetime.now(
                    datetime.timezone.utc
                    ).astimezone() + datetime.timedelta(days=180)
                morsel.update(
                    {'expires': expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT')}
                )  # RFC2109 format
            cookie = requests.cookies.morsel_to_cookie(morsel)
            self._session.cookies.set_cookie(cookie)
        self._session.save_cookiejar()

    def parse(self, args) -> None:
        if args.login and self.login_page:
            self.login()
            return

        if len(args.task) == 1 and self.url_regex.match(args.task[0]):
            url = args.task[0]
            args.inplace = True
        else:
            try:
                url = self.url_finder(args.task)
            except BadTaskError:
                logger.error('Task URL not detected')
                return

        path = './'
        if not args.inplace:
            try:
                task_place = self.placer(args.task)
            except BadTaskError:
                logger.warning('Task place not detected. Creating tests at "%s".', path)
            else:
                confman = ConfigManager()
                path = confman.path_from_root(task_place, makedir=True)

        resp = self._session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        samples = self.sampler(soup)
        if not samples:
            logger.warning("No sample found, make sure you logged in and this url exists")
            return
        sampler.write_samples(samples, path)
