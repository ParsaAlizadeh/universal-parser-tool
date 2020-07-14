from ..util import Util, Driver, By


class Parser:
    TYPE = {"con": "contest",
            "oly": "olympiad",
            "uni": "university"}

    @staticmethod
    def parse(args: list):
        if len(args) != 2:
            raise Exception("Arguments are not correct")

        tp = Parser.TYPE.get(args[0])
        if tp is None:
            raise Exception(f"type \"{args[0]}\" not supported")

        driver = Driver()
        url = f"http://quera.ir/problemset/{tp}/{args[1]}/"
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.even_odd(sample)
        Util.write_samples(result)
