"""
This file supposed to be a documented template for parsers.
You can use this file under WTFPL (http://www.wtfpl.net/txt/copying/)
"""

from typing import Optional, List

from upt.serviceparser import (
    ServiceParser,
    BadTaskError,
    BeautifulSoup,
)
#from upt.sampler import chunkify


# Inheritance from ServiceParser is required
class ExampleParser(ServiceParser):
    @property
    def description(self) -> str:
        # return description of your parser
        return 'Example (https://example.com/)'

    @property
    def login_page(self) -> Optional[str]:
        # return login page if your parser may need logins
        #return 'https://example.com/login/'
        # return None to disable login feature
        return None

    # next 2 functions has task argument
    # task is a tuple of arguments (string) passed to parser

    def url_finder(self, task) -> str:
        # return task URL based on given task
        #return f'http://example.com/problemset/{task[0]}'
        # raise BadTaskError if you can't detect task
        raise BadTaskError()

    def placer(self, task) -> str:
        # return path to the given task
        # this path should be relative to root (configs)
        #return f'example/{task[0]}'
        # raise BadTaskError if you can't detect task
        raise BadTaskError()

    def sampler(self, soup: BeautifulSoup) -> List[List[str]]:
        # return samples from given soup
        # this function returns a list in this format
        # [[input_0, output_0], [input_1, output_1], ...]
        # you may use chunkify here as a utility function
        return []


# register parsers and their aliases
def register():
    return {
        'example': ExampleParser
    }
