from .util import baseparser, sampler

PROBLEM_URL = "http://www.codechef.com/problems/{0}"
PLACE_PATH = "/codechef/{0}"


class Codechef(baseparser.TemplateParser):
    name = "codechef"
    usage = "upt codechef [-h] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__()

    def url_finder(self, task):
        task = task.upper()
        return PROBLEM_URL.format(task)

    def placer(self, task):
        task = task.lower()
        return PLACE_PATH.format(task)

    def sampler(self, elements):
        return sampler.Sampler.tag_sensitive(elements)
