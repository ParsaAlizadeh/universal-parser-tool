from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging, requests


class Utils:
    @staticmethod
    def get_sample(driver: Firefox) -> list:
        """
        After loading web page, this command finds all `<pre>` tags and output list of
        texts in them.
        """
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
        req = requests.get(url)
        req.raise_for_status()

        wait = WebDriverWait(driver, 20)
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "pre")))
        driver.execute_script("window.stop();")
        logging.info("URL loaded")

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
