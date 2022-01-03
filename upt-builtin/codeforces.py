import re

from upt.serviceparser import ServiceParser, BadTaskError, BeautifulSoup
from upt.sampler import chunkify


class Codeforces(ServiceParser):
    @property
    def description(self):
        return 'Codeforces (https://codeforces.com/)'

    @property
    def login_page(self):
        return "https://codeforces.com/enter"

    problem_url = "https://codeforces.com/contest/{0}/problem/{1}"
    gym_url = "https://codeforces.com/gym/{0}/problem/{1}"

    problem_path = "contest/{0}/{1}/"
    gym_path = "gym/{0}/{1}/"

    task_pattern = re.compile(r"^(\d+)(\w\d?)$")

    def get_task_info(self, task):
        match = self.task_pattern.match(task)
        if not match:
            raise BadTaskError('Expect something like "4A"')
        return match.group(1), match.group(2).lower()

    def url_finder(self, task):
        task = "".join(task)
        contest, index = self.get_task_info(task)
        return (self.problem_url if len(contest) < 6 else self.gym_url).format(contest, index)

    def placer(self, task):
        task = "".join(task)
        contest, index = self.get_task_info(task)
        return (self.problem_path if len(contest) < 6 else self.gym_path).format(contest, index)

    def sampler(self, soup: BeautifulSoup):
        expected = ("input", "output")
        sample = []
        for elem in soup.find_all("pre"):
            div = elem.parent
            if div is None or div.get("class") is None:
                continue
            if div.get("class")[0] not in expected:
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
