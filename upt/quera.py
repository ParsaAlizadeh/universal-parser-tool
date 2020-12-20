import re

from markdown import markdown

from .util.baseparser import BaseParser, BeautifulSoup
from .util.sampler import chunkify


class Quera(BaseParser):
    usage = "[-h] [-l] [-i] [task...]"

    problem_type = {"con": "contest",
                    "oly": "olympiad",
                    "uni": "university"}
    login_page = "https://quera.ir/accounts/login"
    problem_url = "http://quera.ir/problemset/{0}/{1}/"
    place_path = "quera/{0}/{1}/"

    statement = re.compile(r"^description_md-")

    def __init__(self, alias):
        super().__init__(alias)

    def url_finder(self, problem_type, index):
        problem_type = self.problem_type.get(problem_type, problem_type)
        return self.problem_url.format(problem_type, index)

    def placer(self, problem_type, index):
        problem_type = self.problem_type.get(problem_type, problem_type)
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
            if header is None or "h" not in header.name or not any(_ in header.text for _ in expected):
                continue
            sample.append("\n".join(elem.strings))
        return chunkify(sample, 2)
