from ..util import parser_common
from ..util.parser_common import By


def __login_checker(driver):
    assert "dashboard" in driver.current_url, "Login failed"


DRIVER_OPTIONS = {"nostrategy": False}
LOGIN_OPTIONS = {"url": "https://quera.ir/accounts/login",
                 "username": (By.NAME, "login"),
                 "password": (By.NAME, "password"),
                 "submit": (By.XPATH, "/html/body/div[3]/div/div/div[1]/form/div[3]"),
                 "checker": __login_checker}
PROBLEM_TYPE = {"con": "contest",
                "oly": "olympiad",
                "uni": "university"}
PROBLEM_URL = "http://quera.ir/problemset/{0}/{1}/"
PLACE_PATH = "/quera/{0}/{1}"


class Quera(parser_common.TemplateParser):
    name = "quera"
    usage = "upt quera [-h] [--init] [-l] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__(login_options=LOGIN_OPTIONS,
                         driver_options=DRIVER_OPTIONS)

    def url_finder(self, problem_type, index):
        problem_type = PROBLEM_TYPE.get(problem_type)
        return PROBLEM_URL.format(problem_type, index)

    def placer(self, problem_type, index):
        problem_type = PROBLEM_TYPE.get(problem_type)
        return PLACE_PATH.format(problem_type, index)
