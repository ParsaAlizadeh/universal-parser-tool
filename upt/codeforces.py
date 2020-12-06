import re

from .util.baseparser import BaseParser, BeautifulSoup, NotRecognizedProblem
from .util.sampler import chunkify

LOGIN_PAGE = "https://codeforces.com/enter"

PROBLEM_URL = "https://codeforces.com/problemset/problem/{0}/{1}/"
GYM_URL = "https://codeforces.com/gym/{0}/problem/{1}"

PROBLEM_PATH = "contest/{0}/{1}/"
GYM_PATH = "gym/{0}/{1}/"


class Codeforces(BaseParser):
    usage = "[-h] [-l] [-i] [-u URL] [task...]"

    def __init__(self, alias):
        super().__init__(alias, login_page=LOGIN_PAGE)
        self.pattern = re.compile(r"(\d+)(\w\d?)")

    def get_task_info(self, task):
        match = self.pattern.match(task)
        if not match:
            raise NotRecognizedProblem()
        return match.group(1), match.group(2).lower()

    def url_finder(self, *task):
        task = "".join(task)
        contest, index = self.get_task_info(task)
        return (PROBLEM_URL if len(contest) < 6 else GYM_URL).format(contest, index)

    def placer(self, *task):
        task = "".join(task)
        contest, index = self.get_task_info(task)
        return (PROBLEM_PATH if len(contest) < 6 else GYM_PATH).format(contest, index)

    def sampler(self, soup: BeautifulSoup):
        expected = ("input", "output")
        sample = []
        for elem in soup.find_all("pre"):
            div = elem.parent
            if div is None or not div["class"] or div["class"][0] not in expected:
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
