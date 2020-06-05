from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging


class PreParser:
    @staticmethod
    def get_sample(driver:Firefox, args=None) -> list:
        elements = driver.find_elements_by_css_selector("pre")
        sample = []
        for elem in elements:
            if len(elem.text) > 0:
                sample.append(elem.text)

        return sample

    @staticmethod
    def load_url(driver, url):
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "pre")))
        driver.execute_script("window.stop();")
        logging.info("URL loaded")