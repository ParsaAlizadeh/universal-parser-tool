from ..serviceparser import ServiceParser, BadTaskError, BeautifulSoup
from ..sampler import chunkify


class Usaco(ServiceParser):
    @property
    def description(self):
        return 'Usaco (https://usaco.org/)'

    @property
    def aliases(self):
        return ('usaco',)

    @property
    def login_page(self):
        return "http://www.usaco.org/"

    def url_finder(self, task):
        raise BadTaskError('No task pattern for usaco. You should use URLs')

    def placer(self, task):
        raise BadTaskError('No task pattern for usaco, You should use URLs')

    def sampler(self, soup: BeautifulSoup):
        expected = ("in", "out")
        sample = []
        for elem in soup.find_all("pre", attrs={"class": expected}):
            sample.append(elem.text)
        return chunkify(sample, 2)
