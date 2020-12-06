import re

from .util.baseparser import BaseParser, BeautifulSoup
from .util.sampler import chunkify

LOGIN_PAGE = "https://atcoder.jp/login"
PROBLEM_URL = "https://atcoder.jp/contests/{0}/tasks/{0}_{1}"
PLACE_PATH = "/atcoder/{0}/{1}"


class AtCoder(BaseParser):
    name = "atcoder"
    usage = "upt atcoder [-h] [-l] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__(login_page=LOGIN_PAGE)

    def url_finder(self, contest, index):
        index = index.lower()
        return PROBLEM_URL.format(contest, index)

    def placer(self, contest, index):
        index = index.lower()
        return PLACE_PATH.format(contest, index)

    def sampler(self, soup: BeautifulSoup):
        pattern = re.compile(r"Sample (In|Out)put")
        sample = []
        for elem in soup.find_all("pre"):
            header = elem.find_previous_sibling()
            if header is None or header.name != "h3" or not pattern.match(header.text):
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
