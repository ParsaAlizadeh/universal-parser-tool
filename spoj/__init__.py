from selenium.webdriver import Firefox

from utils import Utils


class Parser:
    @staticmethod
    def get_sample(driver: Firefox, args: list) -> list:
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        url = f"http://www.spoj.com/problems/{args[0]}/"
        Utils.load_url(driver, url)

        sample = Utils.get_sample(driver)
        return Utils.tag_sens(sample)
