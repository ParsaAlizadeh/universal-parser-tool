import re

from .util.baseparser import BaseParser, BeautifulSoup, NotRecognizedProblem
from .util.sampler import chunkify


class AtCoder(BaseParser):
    description = 'AtCoder (https://atcoder.jp/)'
    login_page = "https://atcoder.jp/login"

    problem_url = "https://atcoder.jp/contests/{0}/tasks/{0}_{1}"
    place_path = "atcoder/{0}/{1}/"
    task_pattern = re.compile(r"(a[brg]c)(\d{,3})(\w)")

    def get_task_info(self, task):
        match = self.task_pattern.match(task)
        if not match:
            raise NotRecognizedProblem()
        contest, index, problem = match.groups()
        contest = contest + "0" * (3 - len(index)) + index
        return contest, problem.lower()

    def url_finder(self, *task):
        task = "".join(task)
        return self.problem_url.format(*self.get_task_info(task))

    def placer(self, *task):
        task = "".join(task)
        return self.place_path.format(*self.get_task_info(task))

    def sampler(self, soup: BeautifulSoup):
        pattern = re.compile(r"Sample (In|Out)put")
        sample = []
        for elem in soup.find_all("pre"):
            header = elem.find_previous_sibling()
            if header is None or header.name != "h3" or not pattern.match(header.text):
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
