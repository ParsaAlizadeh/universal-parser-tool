from selenium.webdriver import Firefox
import re, logging


class Parser:
    @staticmethod
    def get_sample(driver:Firefox, args:list) -> list:
        url = f"https://atcoder.jp/contests/{args[0]}/tasks/{args[0]}_{args[1]}"
        driver.get(url)
        logging.info("URL loaded")

        pattern = re.compile(r"pre\-sample\d")
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if pattern.match(elem.get_attribute("id")) and len(elem.text) > 0:
                sample.append(elem.text)

        if len(sample) % 2 == 1:
            raise Exception("Inputs and Outputs not the same number")

        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])

        return result

    @staticmethod
    def get_structure(args:list) -> list:
        return args