import argparse

from ..util import Util, Driver, By
from ..util.pathparser import PathParser


class Parser:
    usage = "upt cf [-h] [-i] <task>"

    @staticmethod
    def parse(args: list):
        argparser = argparse.ArgumentParser(prog="upt cf",
                                            usage=Parser.usage)
        argparser.add_argument(
            "-i",
            "--inplace",
            help="Create tests inplace instead of root",
            action="store_true")
        argparser.add_argument("task", help="Task name to parse")
        args = argparser.parse_args(args)

        task = args.task.lower()
        if task[-1].isdigit():
            contest, index = task[:-2], task[-2:]
        else:
            contest, index = task[:-1], task[-1]
        path = "./" if args.inplace else PathParser().get_path(
            f"/{contest}/{index}", makedir=True)
        url = f"https://codeforces.com/problemset/problem/{contest}/{index}/"

        driver = Driver()
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.even_odd(sample)
        Util.write_samples(result, path=path)
