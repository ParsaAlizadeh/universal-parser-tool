import logging
import os

from .configmanager import ConfigManager

logger = logging.getLogger("sample")


def chunkify(sequence, batch):
    return [sequence[i:i + batch] for i in range(0, len(sequence), batch)]


def write_sample_to_file(string, filename):
    string = string.strip() + "\n"
    with open(filename, "w") as file:
        file.write(string)


def write_samples(samples: list, root: str = "./"):
    logger.info(
        "Writing %s sample%s into '%s'",
        len(samples),
        's' * bool(len(samples) > 1),
        root
    )
    confman = ConfigManager()
    for path in (confman.input_path(0), confman.output_path(0)):
        main_path = os.path.join(root, path)
        os.makedirs(os.path.dirname(main_path), exist_ok=True)

    for i, sample in enumerate(samples):
        input_path = os.path.join(root, confman.input_path(i+1))
        output_path = os.path.join(root, confman.output_path(i+1))
        write_sample_to_file(sample[0], input_path)
        write_sample_to_file(sample[1], output_path)
