import logging
import os

from selenium.webdriver import Firefox

logger = logging.getLogger("driver")


class Driver(Firefox):  # TODO: Add other browsers
    def __init__(self):
        logger.info("Starting driver")
        super().__init__(service_log_path=os.path.devnull)

    def get(self, url):
        logger.info("Loading '%s'", url)
        super().get(url)
