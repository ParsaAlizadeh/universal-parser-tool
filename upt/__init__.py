import argparse
import logging
import os
import sys

from . import atcoder, codechef, quera, spoj, codeforces
from .util.pathparser import PathParser


PARSERS = {"atcoder": atcoder.Parser,
           "quera": quera.Parser,
           "codechef": codechef.Parser,
           "spoj": spoj.Parser,
           "cf": codeforces.Parser,
           "init": PathParser}


def main():
    logging.basicConfig(level=logging.INFO, format="== [%(levelname)s] %(name)7s: %(message)s")
    logger = logging.getLogger("main")

    argparser = argparse.ArgumentParser(prog="upt")
    argparser.add_argument("parser", help="Parser name")
    argparser.add_argument("command", nargs=argparse.REMAINDER, help="Parser commands")
    args = argparser.parse_args(sys.argv[1:])

    if args.parser not in PARSERS:
        logger.warning(f"No parser named \"{args.parser}\", try running cf ...")
        os.system("cf " + " ".join(sys.argv[1:]))
        return

    logger.info(f"Parser \"{args.parser}\" called")
    main_parser = PARSERS.get(args.parser)()
    main_parser.parse(args.command)
    logger.info(f"Parser \"{args.parser}\" finished")


if __name__ == "__main__":
    main()
