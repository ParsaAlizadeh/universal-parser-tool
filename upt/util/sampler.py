import logging

logger = logging.getLogger("sample")


def chunkify(sequence, batch):
    return [sequence[i:i + batch] for i in range(0, len(sequence), batch)]


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
