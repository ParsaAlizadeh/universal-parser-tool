import re

from ..serviceparser import ServiceParser, BadTaskError, BeautifulSoup
from ..sampler import chunkify


class AtCoder(ServiceParser):
    @property
    def description(self):
        return 'AtCoder (https://atcoder.jp/)'

    @property
    def aliases(self):
        return ('atcoder', 'atc')

    @property
    def login_page(self):
        return "https://atcoder.jp/login"

    problem_url = "https://atcoder.jp/contests/{0}/tasks/{0}_{1}"
    place_path = "atcoder/{0}/{1}/"
    task_pattern = re.compile(r"(a[brg]c) ?(\d{,3}) ?(\w)")

    def get_task_info(self, task):
        match = self.task_pattern.match(task)
        if not match:
            raise BadTaskError('Expect something like "abc208A"')
        contest, index, problem = match.groups()
        contest = contest + "0" * (3 - len(index)) + index
        return contest, problem.lower()

    def url_finder(self, task):
        task = "".join(task).lower()
        task_info = self.get_task_info(task)
        return self.problem_url.format(*task_info)

    def placer(self, task):
        task = "".join(task).lower()
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
