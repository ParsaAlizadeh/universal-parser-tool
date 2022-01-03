import re

from markdown import markdown

from upt.serviceparser import ServiceParser, BadTaskError, BeautifulSoup
from upt.sampler import chunkify


class Quera(ServiceParser):
    @property
    def description(self):
        return 'Quera (https://quera.ir/)'

    @property
    def login_page(self):
        return "https://quera.ir/accounts/login"

    problem_url = "http://quera.ir/problemset/{0}/"
    place_path = "quera/{0}/"
    statement = re.compile(r"^description_md-")

    def get_task_info(self, task):
        if len(task) != 1:
            raise BadTaskError("Except only one argument as a task, like 127292")
        return task[0]

    def url_finder(self, task):
        task = self.get_task_info(task)
        return self.problem_url.format(task)

    def placer(self, task):
        task = self.get_task_info(task)
        return self.place_path.format(task)

    def sampler(self, soup: BeautifulSoup):
        expected = ("ورودی نمونه", "خروجی نمونه")
        desc = soup.find(id=self.statement)
        if desc is None:
            return []
        md_soup = BeautifulSoup(markdown(desc.text), 'html.parser')
        sample = []
        for elem in md_soup.find_all("code"):
            if elem.parent is None:
                continue
            header = elem.parent.find_previous_sibling()
            if header is not None and any(_ in header.text for _ in expected):
                sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
