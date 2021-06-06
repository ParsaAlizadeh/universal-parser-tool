import re

from .util.baseparser import BaseParser, BeautifulSoup, NotRecognizedProblem
from .util.sampler import chunkify


class Usaco(BaseParser):
    description = 'Usace (https://usaco.org/)'
    login_page = "http://www.usaco.org/"

    task_pattern = re.compile(r"(a[brg]c)(\d{,3})(\w)")

    def url_finder(self, *task):
        raise NotRecognizedProblem()

    def placer(self, *task):
        raise NotRecognizedProblem()

    def sampler(self, soup: BeautifulSoup):
        expected = ("in", "out")
        sample = []
        for elem in soup.find_all("pre", attrs={"class": expected}):
            sample.append(elem.text)
        return chunkify(sample, 2)
