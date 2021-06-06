import re

from .util.baseparser import BaseParser, BeautifulSoup, NotRecognizedProblem
from .util.sampler import chunkify


class Codeforces(BaseParser):
    description = 'Codeforces (https://codeforces.com/)'
    login_page = "https://codeforces.com/enter"

    problem_url = "https://codeforces.com/problemset/problem/{0}/{1}/"
    gym_url = "https://codeforces.com/gym/{0}/problem/{1}"

    problem_path = "contest/{0}/{1}/"
    gym_path = "gym/{0}/{1}/"

    task_pattern = re.compile(r"(\d+)(\w\d?)")

    def get_task_info(self, task):
        match = self.task_pattern.match(task)
        if not match:
            raise NotRecognizedProblem()
        return match.group(1), match.group(2).lower()

    def url_finder(self, *task):
        task = "".join(task)
        contest, index = self.get_task_info(task)
        return (self.problem_url if len(contest) < 6 else self.gym_url).format(contest, index)

    def placer(self, *task):
        task = "".join(task)
        contest, index = self.get_task_info(task)
        return (self.problem_path if len(contest) < 6 else self.gym_path).format(contest, index)

    def sampler(self, soup: BeautifulSoup):
        expected = ("input", "output")
        sample = []
        for elem in soup.find_all("pre"):
            div = elem.parent
            if div is None or not div["class"] or div["class"][0] not in expected:
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
