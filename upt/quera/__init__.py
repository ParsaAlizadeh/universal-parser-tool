import argparse

from ..util import Util, Driver, By


class Parser:
    TYPE = {"con": "contest",
            "oly": "olympiad",
            "uni": "university"}

    @staticmethod
    def parse(args: list):
        argparser = argparse.ArgumentParser(prog="upt quera",
                                            description="example: upt quera oly 34406")
        argparser.add_argument("type", help="Task type")
        argparser.add_argument("code", help="Task code")
        args = argparser.parse_args(args)

        assert args.type in Parser.TYPE, f"Type \"{args.type}\" not supported"

        tp = Parser.TYPE.get(args.type)
        url = f"http://quera.ir/problemset/{tp}/{args.code}/"

        driver = Driver()
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.even_odd(sample)
        Util.write_samples(result)
