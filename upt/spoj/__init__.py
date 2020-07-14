from ..util import Util, Driver, By


class Parser:
    @staticmethod
    def parse(args: list):
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        driver = Driver()
        url = f"http://www.spoj.com/problems/{args[0]}/"
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.tag_sens(sample)
        Util.write_samples(result)
