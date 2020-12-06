import re

from .util.baseparser import BaseParser, BeautifulSoup
from .util.sampler import chunkify

LOGIN_PAGE = "https://codeforces.com/enter"
PROBLEM_URL = "https://codeforces.com/problemset/problem/{0}/{1}/"
PLACE_PATH = "/contest/{0}/{1}"


class Codeforces(BaseParser):
    usage = "[-h] [-l] [-i] [-u URL] [task...]"

    def __init__(self, alias):
        super().__init__(alias, login_page=LOGIN_PAGE)
        self.__pattern = re.compile(r"(\d+)(\w\d?)")

    def get_task_info(self, task):
        match = self.__pattern.match(task)
        if not match:
            return None
        return match.groups()

    def url_finder(self, task):
        contest, index = self.get_task_info(task)
        return PROBLEM_URL.format(contest, index)

    def placer(self, task):
        contest, index = self.get_task_info(task)
        return PLACE_PATH.format(contest, index)

    def sampler(self, soup: BeautifulSoup):
        expected = ("input", "output")
        sample = []
        for elem in soup.find_all("pre"):
            div = elem.parent
            if div is None or not div["class"] or div["class"][0] not in expected:
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
