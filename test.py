from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import os, re, sys
import logging

logging.basicConfig(level=logging.INFO)

options = Options()
options.add_argument("--headless")

driver = Firefox(options=options)
logging.info("Driver Loaded")

args = sys.argv[1:]
url = f"https://atcoder.jp/contests/{args[0]}/tasks/{args[0]}_{args[1]}"

driver.get(url)
logging.info("URL Loaded")

pat = re.compile(r"pre\-sample\d")
elems = driver.find_elements_by_css_selector("pre")
sample = []
for elem in elems:
    if pat.match(elem.get_attribute("id")) and len(elem.text) > 0:
        sample.append(elem.text)

result = []
for i in range(0, len(sample), 2):
    result.append([sample[i], sample[i + 1]])

print(result)

driver.quit()
logging.info("Driver Closed")