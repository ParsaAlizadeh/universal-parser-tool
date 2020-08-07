import logging
import os
from os.path import expanduser

from selenium.webdriver import Firefox
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # needed in atcoder and quera

logger = logging.getLogger("util")
CONFIG = expanduser("~/.uptrc")


class Driver(Firefox):
    def __init__(self, nostrategy=True):
        logger.info("Loading driver")
        capa = DesiredCapabilities.FIREFOX
        if nostrategy:
            capa["pageLoadStrategy"] = "none"
        opt = Options()
        opt.add_argument("--headless")
        super().__init__(options=opt,
                         desired_capabilities=capa,
                         service_log_path=os.path.devnull)

    def __del__(self):
        logger.info("Quiting driver")
        self.quit()

    def get(self, url):
        logger.info("Loading URL")
        super().get(url)


class Util:
    @staticmethod
    def get_sample(driver: Firefox) -> list:
        logger.info("Reading samples")
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if len(elem.text) > 0:
                sample.append(elem.text)
        return sample

    @staticmethod
    def wait_until(driver, by, name):
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((by, name)))
        driver.execute_script("window.stop();")

    @staticmethod
    def even_odd(sample: list) -> list:
        if len(sample) % 2 == 1:
            raise Exception("Found odd number of samples")

        result = []
        for i in range(0, len(sample), 2):
            result.append([sample[i], sample[i + 1]])

        return result

    @staticmethod
    def tag_sens(sample: list, inp: str = "Input:\n",
                 out: str = "Output:\n") -> list:
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
    def write_samples(samples: list, path: str = "./"):
        if path[-1] != "/":
            path = path + "/"
        logger.info("Writing samples into " + path)
        for i in range(len(samples)):
            Util.write_to_file(samples[i][0], path + f"in{i}.txt")
            Util.write_to_file(samples[i][1], path + f"ans{i}.txt")
