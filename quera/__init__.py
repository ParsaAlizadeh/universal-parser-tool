from selenium.webdriver import Firefox
from preparser import PreParser


class Parser:
    @staticmethod
    def get_sample(driver:Firefox, args:list) -> list:
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        url = f"http://quera.ir/problemset/contest/{args[0]}/"
        PreParser.load_url(driver, url)

        sample = PreParser.get_sample(driver)

        if len(sample) % 2 == 1:
            raise Exception("found odd number of <pre> elements")

        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])

        return result