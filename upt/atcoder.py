import re

from .util.baseparser import BaseParser

LOGIN_PAGE = "https://atcoder.jp/login"
PROBLEM_URL = "https://atcoder.jp/contests/{0}/tasks/{0}_{1}"
PLACE_PATH = "/atcoder/{0}/{1}"


class AtCoder(BaseParser):
    name = "atcoder"
    usage = "upt atcoder [-h] [--init] [-l] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__(login_page=LOGIN_PAGE)

    def url_finder(self, contest, index):
        index = index.lower()
        return PROBLEM_URL.format(contest, index)

    def placer(self, contest, index):
        index = index.lower()
        return PLACE_PATH.format(contest, index)

    def sampler(self, soup):
        pattern = re.compile(r"pre\-sample\d")
        sample = []
        for elem in elements:
            if pattern.match(elem["id"]) and elem.text:
                sample.append(elem.text)
        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])
        return result
