import logging
import os
import sys

from upt import quera, atcoder, codechef, spoj

PARSERS = {"atcoder": atcoder,
           "quera": quera,
           "codechef": codechef,
           "spoj": spoj}


def excepthook(type, value, traceback):
    logging.error(value)


def main():
    sys.excepthook = excepthook
    logging.basicConfig(level=logging.INFO, format="== [%(levelname)s] %(message)s")

    args = sys.argv[1:]

    if len(args) < 2:
        raise Exception("arguments not enough")

    main_parser = PARSERS.get(args[0])
    if main_parser is None:
        raise Exception(f"Parser \"{args[0]}\" not found")

    main_parser = main_parser.Parser

    logging.info(f"Parser \"{args[0]}\" called")
    main_parser.parse(args[1:])
    logging.info(f"Parser \"{args[0]}\" finished")


if __name__ == "__main__":
    main()
