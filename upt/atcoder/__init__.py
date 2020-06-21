import re
from upt.utils import Utils, Driver


class Parser:
    @staticmethod
    def parse(args: list):
        if len(args) != 2:
            raise Exception("arguments are not correct")

        driver = Driver()
        url = f"http://atcoder.jp/contests/{args[0]}/tasks/{args[0]}_{args[1]}"
        Utils.load_url(driver, url)

        pattern = re.compile(r"pre\-sample\d")
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and len(elem.text) > 0:
                sample.append(elem.text)

        result = Utils.even_odd(sample)
        Utils.write_samples(result)
