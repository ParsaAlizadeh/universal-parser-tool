import logging
import os
import pickle

import requests

from .constants import COOKIE_FILE

logger = logging.getLogger("session")


class Session(requests.Session):
    def __init__(self):
        super().__init__()
        self.load_cookiejar()

    def load_cookiejar(self):
        if not os.path.exists(COOKIE_FILE):
            return
        with open(COOKIE_FILE, "rb") as file:
            self.cookies.update(pickle.load(file))

    def save_cookiejar(self):
        with open(COOKIE_FILE, "wb") as file:
            pickle.dump(self.cookies, file)

    def get(self, url, **kwargs):
        logger.info("GET '%s'", url)
        resp = super().get(url, **kwargs)
        logger.info("Return HTTP Code %s", resp.status_code)
        resp.raise_for_status()
        return resp
