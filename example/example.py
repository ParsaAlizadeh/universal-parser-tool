"""
This file supposed to be a documented template for parsers.
You can use this file under WTFPL (http://www.wtfpl.net/txt/copying/)
"""

# necessary imports
from upt.util.baseparser import (
    BaseParser,
    BeautifulSoup,
    NotRecognizedProblem,
)
from upt.util.sampler import chunkify


class ExampleParser(BaseParser):
    # description of your parser
    description = 'Example (https://example.com/)'

    # login page if your parser may need logins
    login_page = 'https://example.com/login/'
    # set login_page to None to disable login feature
    login_page = None

    # next 2 functions has *task argument
    # task is a tuple of arguments (string) passed to parser
    def url_finder(self, *task):
        """ return task url based on given arguments """
        # you can raise NotRecognizedProblem if passed argument is wrong
        raise NotRecognizedProblem()

    def placer(self, *task):
        """ return path to the given task """
        # this path should be relative to root (configs)
        # raise NotRecognizedProblem for wrong arguments
        raise NotRecognizedProblem()

    def sampler(self, soup: BeautifulSoup):
        """ return samples from given soup """
        # this function returns a list in this format
        # [[input_0, output_0], [input_1, output_1], ...]
        # you may use chunkify as a utility function
        return []
