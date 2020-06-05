from selenium.webdriver import Firefox
import logging
from preparser import PreParser


class Parser(PreParser):
    @staticmethod
    def get_sample(driver:Firefox, args:list) -> list:
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        url = f"http://quera.ir/problemset/contest/{args[0]}/"
        driver.get(url)
        logging.info("URL loaded")

        return super().get_sample(driver, args)