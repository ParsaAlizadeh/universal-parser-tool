from upt.utils import Utils, Driver


class Parser:
    @staticmethod
    def parse(args: list):
        if len(args) != 1:
            raise Exception("arguments are not correct")

        driver = Driver()
        url = f"http://www.spoj.com/problems/{args[0]}/"
        Utils.load_url(driver, url)

        sample = Utils.get_sample(driver)
        result = Utils.tag_sens(sample)
        Utils.write_samples(result)
