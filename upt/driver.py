import logging
import os

from selenium.common.exceptions import WebDriverException
from selenium import webdriver

logger = logging.getLogger("driver")


class NoWebDriverError(Exception):
    pass

def get_webdriver():
    webdrivers = {
        'Firefox': webdriver.Firefox,
        'Chrome': webdriver.Chrome,
        'Safari': webdriver.Safari,
        'Edge': webdriver.Edge,
    }
    for name, Driver in webdrivers.items():
        logger.info('Trying %s...', name)
        try:
            return Driver() if name == 'Safari' else Driver(service_log_path=os.path.devnull)
        except WebDriverException as e:
            logger.warning(e.msg)
        except Exception as e:
            logger.warning(str(e).strip())

    raise NoWebDriverError(
        'Unable to find a webdriver. Make sure you installed drivers based on your browser.'
    )
