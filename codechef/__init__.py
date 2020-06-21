from selenium.webdriver import Firefox

from utils import Utils


class Parser:
    @staticmethod
    def parse(driver: Firefox, args: list):
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        url = f"http://www.codechef.com/problems/{args[0]}"
        Utils.load_url(driver, url)

        sample = Utils.get_sample(driver)
        result = Utils.tag_sens(sample)
        Utils.write_samples(result)
