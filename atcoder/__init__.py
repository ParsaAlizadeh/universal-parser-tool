import re

from selenium.webdriver import Firefox

from utils import Utils


class Parser:
    @staticmethod
    def get_sample(driver: Firefox, args: list) -> list:
        if len(args) != 2:
            raise Exception("Arguments are not correct")

        url = f"http://atcoder.jp/contests/{args[0]}/tasks/{args[0]}_{args[1]}"
        Utils.load_url(driver, url)

        pattern = re.compile(r"pre\-sample\d")
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and len(elem.text) > 0:
                sample.append(elem.text)

        return Utils.even_odd(sample)
