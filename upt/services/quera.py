import re

from markdown import markdown

from ..serviceparser import ServiceParser, BadTaskError, BeautifulSoup
from ..sampler import chunkify


class Quera(ServiceParser):
    @property
    def description(self):
        return 'Quera (https://quera.ir/)'

    @property
    def aliases(self):
        return ('quera',)

    @property
    def login_page(self):
        return "https://quera.ir/accounts/login"

    problem_type = {"con": "contest",
                    "oly": "olympiad",
                    "uni": "university"}
    problem_url = "http://quera.ir/problemset/{0}/{1}/"
    place_path = "quera/{0}/{1}/"
    statement = re.compile(r"^description_md-")

    def get_type(self, problem_type):
        if problem_type in self.problem_type:
            problem_type = self.problem_type.get(problem_type)
        elif problem_type not in self.problem_type.values:
            raise BadTaskError('Expect something like "olympiad 66756"')
        return problem_type

    def url_finder(self, task):
        problem_type, index = task
        problem_type = self.get_type(problem_type)
        return self.problem_url.format(problem_type, index)

    def placer(self, task):
        problem_type, index = task
        problem_type = self.get_type(problem_type)
        return self.place_path.format(problem_type, index)

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
