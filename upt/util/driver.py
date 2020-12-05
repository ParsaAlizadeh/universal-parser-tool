import logging
import os

from selenium.webdriver import Firefox

logger = logging.getLogger("driver")


class Driver(Firefox):
    def __init__(self, nostrategy=True):
        logger.info("Loading driver")
        super().__init__(service_log_path=os.path.devnull)

    def __del__(self):
        logger.info("Quiting driver")
        self.quit()

    def get(self, url):
        logger.info(f"Loading '{url}'")
        super().get(url)
