import re

from ..util import parser_common
from ..util.parser_common import By


def __login_checker(driver):
    parser_common.wait_until(driver, By.CSS_SELECTOR, ".alert")
    alert = driver.find_element_by_css_selector(".alert")
    assert "Welcome" in alert.text, "Login failed"


LOGIN_OPTIONS = {"url": "https://atcoder.jp/login",
                 "username": (By.ID, "username"),
                 "password": (By.ID, "password"),
                 "submit": (By.ID, "submit"),
                 "checker": __login_checker}
PROBLEM_URL = "https://atcoder.jp/contests/{0}/tasks/{0}_{1}"
PLACE_PATH = "/atcoder/{0}/{1}"


class AtCoder(parser_common.TemplateParser):
    name = "atcoder"
    usage = "upt atcoder [-h] [--init] [-l] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__(login_options=LOGIN_OPTIONS)

    def url_finder(self, contest, index):
        index = index.lower()
        return PROBLEM_URL.format(contest, index)

    def placer(self, contest, index):
        index = index.lower()
        return PLACE_PATH.format(contest, index)

    def sampler(self, elements):
        pattern = re.compile(r"pre\-sample\d")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and elem.text:
                sample.append(elem.text)
        assert len(sample) % 2 == 0, "Found odd number of samples"
        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])
        return result
