import logging
import os

from selenium.webdriver import Firefox
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

logger = logging.getLogger("driver")


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
        logger.info(f"Loading '{url}'")
        super().get(url)
