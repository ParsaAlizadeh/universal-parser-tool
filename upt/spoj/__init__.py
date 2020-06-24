from upt.utils import Utils, Driver, By


class Parser:
    @staticmethod
    def parse(args: list):
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        driver = Driver()
        url = f"http://www.spoj.com/problems/{args[0]}/"
        driver.get(url)
        Utils.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Utils.get_sample(driver)
        result = Utils.tag_sens(sample)
        Utils.write_samples(result)
