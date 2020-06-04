from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from atcoder import atcoder
import os, sys, logging


def write_to_file(string:str, filename:str):
    if string[-1] != '\n':
        string += '\n'
    with open(filename, "w") as file:
        file.write(string)


def init_cwd(struc:list) -> str:
    cwd = os.getcwd()
    pos = '/'.join(struc)
    if cwd.find(pos) != -1:
        return "./"
    for i in range(len(struc)):
        os.mkdir('/'.join(struc[:i + 1]))
    return pos + "/"


logging.basicConfig(level=logging.INFO)
PARSERS = {"atcoder": atcoder}

opt = Options()
opt.add_argument("--headless")
driver = Firefox(options=opt)
logging.info("Driver loaded")

args = sys.argv[1:]
Parser = PARSERS[args[0]].Parser

struc = Parser.get_structure(args[1:])
pos = init_cwd(struc)
os.chdir(pos)
logging.info("Directory structure init")
logging.info(pos)

result = Parser.get_sample(driver, args[1:])
logging.info("Samples parsed")
for i in range(len(result)):
    write_to_file(result[i][0], f"in{i}.txt")
    write_to_file(result[i][1], f"ans{i}.txt")

os.system("cf gen")

driver.quit()