from selenium.webdriver import Firefox

from utils import Utils


class Parser:
    TYPE = {"con": "contest",
            "oly": "olympiad",
            "uni": "university"}

    @staticmethod
    def parse(driver: Firefox, args: list):
        if len(args) != 2:
            raise Exception("arguments are not correct")

        tp = Parser.TYPE.get(args[0])
        if tp is None:
            raise Exception(f"type \"{args[0]}\" not supported")

        url = f"http://quera.ir/problemset/{tp}/{args[1]}/"
        Utils.load_url(driver, url)

        sample = Utils.get_sample(driver)
        result = Utils.even_odd(sample)
        Utils.write_samples(result)
