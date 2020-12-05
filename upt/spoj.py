from .util import baseparser, sampler

PROBLEM_URL = "http://www.spoj.com/problems/{0}/"
PLACE_PATH = "/spoj/{0}"


class Spoj(baseparser.TemplateParser):
    name = "spoj"
    usage = "upt spoj [-h] [-i] [-u URL] [task...]"

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
