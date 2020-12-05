import requests
import pickle
import os
import logging

from . import COOKIE_FILE

logger = logging.getLogger("session")


class Session(requests.Session):
    def __init__(self):
        super().__init__()
        self.load_cookiejar()

    def load_cookiejar(self):
        if not os.path.exists(COOKIE_FILE):
            logger.info("No pre-saved cookies")
            return
        with open(COOKIE_FILE, "rb") as file:
            self.cookies.update(pickle.load(file))

    def save_cookiejar(self):
        with open(COOKIE_FILE, "wb") as file:
            pickle.dump(self.cookies, file)
