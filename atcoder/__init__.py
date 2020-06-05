from selenium.webdriver import Firefox
from preparser import PreParser
import re


class Parser:
    @staticmethod
    def get_sample(driver:Firefox, args:list) -> list:
        if len(args) != 2:
            raise Exception("Arguments are not correct")

        url = f"http://atcoder.jp/contests/{args[0]}/tasks/{args[0]}_{args[1]}"
        PreParser.load_url(driver, url)

        pattern = re.compile(r"pre\-sample\d")
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and len(elem.text) > 0:
                sample.append(elem.text)

        if len(sample) % 2 == 1:
            raise Exception("found odd number of <pre> elements")

        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])

        return result