from .util.baseparser import BaseParser, BeautifulSoup
from .util.sampler import chunkify
from markdown import markdown
import re

PROBLEM_TYPE = {"con": "contest",
                "oly": "olympiad",
                "uni": "university"}
LOGIN_PAGE = "https://quera.ir/accounts/login"
PROBLEM_URL = "http://quera.ir/problemset/{0}/{1}/"
PLACE_PATH = "/quera/{0}/{1}"


class Quera(BaseParser):
    name = "quera"
    usage = "upt quera [-h] [-l] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__(login_page=LOGIN_PAGE)

    def url_finder(self, problem_type, index):
        problem_type = PROBLEM_TYPE.get(problem_type, problem_type)
        return PROBLEM_URL.format(problem_type, index)

    def placer(self, problem_type, index):
        problem_type = PROBLEM_TYPE.get(problem_type, problem_type)
        return PLACE_PATH.format(problem_type, index)

    def sampler(self, soup: BeautifulSoup):
        expected = ("ورودی نمونه", "خروجی نمونه")
        desc = soup.find(id=re.compile(r"^description_md-"))
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
