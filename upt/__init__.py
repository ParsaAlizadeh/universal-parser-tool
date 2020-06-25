import logging
import os
import sys

from . import atcoder, codechef, quera, spoj


PARSERS = {"atcoder": atcoder,
           "quera": quera,
           "codechef": codechef,
           "spoj": spoj}


def main():
    logging.basicConfig(level=logging.INFO, format="== [%(levelname)s] %(name)7s: %(message)s")
    logger = logging.getLogger("main")

    args = sys.argv[1:]
    main_parser = PARSERS.get(args[0])
    if main_parser is None:
        raise Exception(f"Parser \"{args[0]}\" not found")

    main_parser = main_parser.Parser()

    logger.info(f"Parser \"{args[0]}\" called")
    main_parser.parse(args[1:])
    logger.info(f"Parser \"{args[0]}\" finished")


if __name__ == "__main__":
    main()
