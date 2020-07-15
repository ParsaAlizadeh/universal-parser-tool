from ..util import Util, Driver, By
from ..util.pathparser import PathParser

class Parser:
    @staticmethod
    def parse(args: list):
        path = None
        if "-h" in args:
            path = "./"
            args.remove("-h")

        assert len(args) == 1, "Arguments are not correct"

        args[0] = args[0].lower()
        name, index = args[0][:-1], args[0][-1]
        url = f"https://codeforces.com/problemset/problem/{name}/{index}/"
        path = PathParser().get_path(f"/{name}/{index}", makedir=True) if path is None else path

        driver = Driver()
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")
        
        sample = Util.get_sample(driver)
        result = Util.even_odd(sample)
        Util.write_samples(result, path=path)
