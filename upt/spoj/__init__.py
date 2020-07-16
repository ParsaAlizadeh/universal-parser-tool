import argparse

from ..util import Util, Driver, By


class Parser:
    @staticmethod
    def parse(args: list):
        argparser = argparse.ArgumentParser(prog="upt spoj",
                                            description="example: upt spoj XMAX")
        argparser.add_argument("task", help="Task name to parse")
        args = argparser.parse_args(args)

        url = f"http://www.spoj.com/problems/{args.task}/"

        driver = Driver()
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.tag_sens(sample)
        Util.write_samples(result)
