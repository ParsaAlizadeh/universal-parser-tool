import logging
import os
import sys

from selenium.webdriver import Firefox
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

import atcoder
import codechef
import quera
import spoj

PARSERS = {"atcoder": atcoder,
           "quera": quera,
           "codechef": codechef,
           "spoj": spoj}


def write_to_file(string: str, filename: str):
    string = string.strip() + "\n"
    with open(filename, "w") as file:
        file.write(string)


def excepthook(type, value, traceback):
    logging.error(value)


sys.excepthook = excepthook
logging.basicConfig(level=logging.INFO, format="== [%(levelname)s] %(message)s")

args = sys.argv[1:]

if len(args) < 2:
    raise Exception("Arguments not enough")

main_parser = PARSERS.get(args[0])
if main_parser is None:
    raise Exception(f"Parser \"{args[0]}\" not found")

main_parser = main_parser.Parser

capa = DesiredCapabilities.FIREFOX
capa["pageLoadStrategy"] = "none"
opt = Options()
opt.add_argument("--headless")
driver = Firefox(options=opt, desired_capabilities=capa)
logging.info("driver loaded")

logging.info(f"Parser \"{args[0]}\" called")
result = main_parser.get_sample(driver, args[1:])
logging.info("samples parsed")

for i in range(len(result)):
    write_to_file(result[i][0], f"in{i}.txt")
    write_to_file(result[i][1], f"ans{i}.txt")

os.system("rm *.log")
logging.info("all logs removed")

os.system("cf gen")

driver.quit()
