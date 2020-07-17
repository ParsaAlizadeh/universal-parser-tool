import argparse

from ..util import Util, Driver, By


class Parser:
    usage = "upt codechef [-h] <task>"

    @staticmethod
    def parse(args: list):
        argparser = argparse.ArgumentParser(prog="upt codechef",
                                            usage=Parser.usage)
        argparser.add_argument("task", help="Task name to parse")
        args = argparser.parse_args(args)

        driver = Driver()
        url = f"http://www.codechef.com/problems/{args.task}"
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.tag_sens(sample)
        Util.write_samples(result)
