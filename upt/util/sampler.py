import logging
import os

from .initparser import InitParser

logger = logging.getLogger("sample")


def chunkify(sequence, batch):
    return [sequence[i:i + batch] for i in range(0, len(sequence), batch)]


def write_sample_to_file(string, filename):
    string = string.strip() + "\n"
    with open(filename, "w") as file:
        file.write(string)


def write_samples(samples: list, path: str = "./"):
    logger.info(
        "Writing %s sample%s into '%s'",
        len(samples),
        's' * bool(len(samples) > 1),
        path
    )
    parser = InitParser(alias=None)

    for func in [parser.get_input, parser.get_output]:
        try:
            main_path = os.path.join(path, func(0))
            os.makedirs(os.path.dirname(main_path))
        except OSError:
            pass

    for i, sample in enumerate(samples):
        input_path = os.path.join(path, parser.get_input(i + 1))
        output_path = os.path.join(path, parser.get_output(i + 1))
        write_sample_to_file(sample[0], input_path)
        write_sample_to_file(sample[1], output_path)
