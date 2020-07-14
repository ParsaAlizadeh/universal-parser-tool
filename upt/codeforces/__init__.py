from ..util import Util, Driver, By


class Parser:
    @staticmethod
    def parse(args: list):
        if len(args) != 1:
            raise Exception("Arguments are not correct")
        
        driver = Driver()
        name, index = args[0][:-1], args[0][-1]
        url = f"https://codeforces.com/problemset/problem/{name}/{index}/"
        driver.get(url)
        Util.wait_until(driver, By.CSS_SELECTOR, "pre")

        sample = Util.get_sample(driver)
        result = Util.even_odd(sample)
        Util.write_samples(result)
