from selenium.webdriver import Firefox

from utils import Utils


class Parser:
    @staticmethod
    def get_sample(driver: Firefox, args: list) -> list:
        if len(args) != 1:
            raise Exception("Arguments are not correct")

        url = f"http://www.codechef.com/problems/{args[0]}"
        Utils.load_url(driver, url)

        sample = Utils.get_sample(driver)

        s1 = "Input:\n"
        s2 = "Output:\n"
        result = []
        for prt in sample:
            ind1 = prt.find(s1)
            ind2 = prt.find(s2)

            result.append([prt[ind1 + len(s1): ind2], prt[ind2 + len(s2):]])

        return result
