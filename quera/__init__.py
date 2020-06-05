from selenium.webdriver import Firefox
import re, logging


class Parser:
    @staticmethod
    def get_sample(driver:Firefox, args:list) -> list:
        logging.warn("Make sure that there is no <pre> other than input/output")
        url = f"http://quera.ir/problemset/contest/{args[0]}/"
        driver.get(url)
        logging.info("URL loaded")

        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if len(elem.text) > 0:
                sample.append(elem.text)

        if len(sample) % 2 == 1:
            raise Exception("Inputs and Outputs not the same number")

        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])

        return result