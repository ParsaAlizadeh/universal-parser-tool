from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import logging
import requests


class Driver(Firefox):
    def __init__(self):
        logging.info("loading driver")
        capa = DesiredCapabilities.FIREFOX
        capa["pageLoadStrategy"] = "none"
        opt = Options()
        opt.add_argument("--headless")
        super().__init__(options=opt, desired_capabilities=capa)

    def __del__(self):
        logging.info("quiting driver")
        self.quit()


class Utils:
    @staticmethod
    def get_sample(driver: Firefox) -> list:
        """
        After loading web page, this command finds all `<pre>` tags and output list of
        texts in them.
        """
        logging.info("reading samples")
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if len(elem.text) > 0:
                sample.append(elem.text)
        return sample

    @staticmethod
    def load_url(driver, url):
        """
        If your parser depends on `<pre>` tags, it is good to use this method instead of
        `driver.get(url)`. In this way, driver just wait for loading `<pre>` tags. So it
        is faster than normal mode.
        """
        logging.info("loading URL")
        req = requests.get(url)
        req.raise_for_status()

        wait = WebDriverWait(driver, 20)
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "pre")))
        driver.execute_script("window.stop();")

    @staticmethod
    def even_odd(sample: list) -> list:
        """
        Let sample be the list of all pre tags, then this method consider even index as
        input and odd index as output.
        """
        if len(sample) % 2 == 1:
            raise Exception("found odd number of samples")

        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])

        return result

    @staticmethod
    def tag_sens(sample: list, inp: str = "Input:\n", out: str = "Output:\n") -> list:
        """
        If pre tags has a flag like `Input` to specify input or output, using this command
        will generate the result. `inp` and `out` are the flags for input and output.
        """
        result = []
        for prt in sample:
            ind1 = prt.find(inp)
            ind2 = prt.find(out)
            result.append([prt[ind1 + len(inp): ind2], prt[ind2 + len(out):]])
        return result

    @staticmethod
    def write_to_file(string: str, filename: str):
        string = string.strip() + "\n"
        with open(filename, "w") as file:
            file.write(string)

    @staticmethod
    def write_samples(samples: list):
        logging.info("writing samples")
        for i in range(len(samples)):
            Utils.write_to_file(samples[i][0], f"in{i + 1}.txt")
            Utils.write_to_file(samples[i][1], f"ans{i + 1}.txt")
