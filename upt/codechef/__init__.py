from ..util import parser_common, sample_common

PROBLEM_URL = "http://www.codechef.com/problems/{0}"
PLACE_PATH = "/codechef/{0}"


class Codechef(parser_common.TemplateParser):
    name = "codechef"
    usage = "upt codechef [-h] [-i] [-u URL] [task...]"

    def __init__(self):
        super().__init__()

    def url_finder(self, task):
        task = task[0].upper()
        return PROBLEM_URL.format(task)

    def placer(self, task):
        task = task[0].lower()
        return PLACE_PATH.format(task)

    def sampler(self, elements):
        return sample_common.Sampler.tag_sensitive(elements)
