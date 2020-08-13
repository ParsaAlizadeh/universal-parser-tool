from ..util import parser_common

PROBLEM_URL = "https://codeforces.com/problemset/problem/{0}/{1}/"
PLACE_PATH = "/contest/{0}/{1}"


class Codeforces(parser_common.TemplateParser):
    name = "cf"
    usage = "upt cf [-h] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_task_info(task):
        task = task.lower()
        if task[-1].isdigit():
            return int(task[:-2]), task[-2:]
        return int(task[:-1]), task[-1:]

    def url_finder(self, task):
        contest, index = Codeforces.get_task_info(task)
        return PROBLEM_URL.format(contest, index)

    def placer(self, task):
        contest, index = Codeforces.get_task_info(task)
        return PLACE_PATH.format(contest, index)
