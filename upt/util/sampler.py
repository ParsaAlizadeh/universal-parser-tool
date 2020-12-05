import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("sample")


class Sampler:
    @staticmethod
    def even_odd(soup: BeautifulSoup):
        elements = soup.find_all("pre")
        if len(elements) % 2 == 1:
            logger.warning("Found odd number of samples, skipping the first one")
            elements = elements[1:]

        result = []
        for i in range(0, len(elements), 2):
            result.append([elements[i].text, elements[i + 1].text])

        return result

    @staticmethod
    def tag_sensitive(soup: BeautifulSoup, inp="Input:\n", out="Output:\n"):
        elements = soup.find_all("pre")
        result = []
        for elem in elements:
            prt = elem.text
            ind1 = prt.find(inp)
            ind2 = prt.find(out)
            result.append([prt[ind1 + len(inp): ind2], prt[ind2 + len(out):]])
        return result


def __write_sample_to_file(string, filename):
    string = string.strip() + "\n"
    with open(filename, "w") as file:
        file.write(string)


def write_samples(samples: list, path: str = "./"):
    if path[-1] != "/":
        path = path + "/"
    logger.info(f"Writing {len(samples)} sample(s) into '{path}'")
    for i in range(len(samples)):
        __write_sample_to_file(samples[i][0], path + f"in{i}.txt")
        __write_sample_to_file(samples[i][1], path + f"ans{i}.txt")
