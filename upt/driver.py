import logging
import os

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome, Edge, Firefox, Opera, Safari

logger = logging.getLogger("driver")


class NoWebDriverError(Exception):
    pass

def get_webdriver():
    webdrivers = {
        'Firefox': Firefox,
        'Chrome': Chrome,
        'Opera': Opera,
        'Safari': Safari,
        'Edge': Edge,
    }
    for name, Driver in webdrivers.items():
        logger.info('Trying %s...', name)
        try:
            return Driver() if Driver is Safari else Driver(service_log_path=os.path.devnull)
        except WebDriverException as e:
            logger.warning(e.msg)
        except Exception as e:
            logger.warning(str(e).strip())

    raise NoWebDriverError(
        'Unable to find a webdriver. Make sure you installed drivers based on your browser.'
    )
