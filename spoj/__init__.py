from selenium.webdriver import Firefox

from preparser import PreParser


class Parser:
    @staticmethod
    def get_sample(driver: Firefox, args: list) -> list:
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        url = f"http://www.spoj.com/problems/{args[0]}/"
        PreParser.load_url(driver, url)

        sample = PreParser.get_sample(driver)
        return PreParser.tag_sens(sample)
