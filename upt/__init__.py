__name__ = "universal-parser-tool"
__version__ = "3.1.1"

import argparse
import logging
import sys

from .atcoder import AtCoder
from .codeforces import Codeforces
from .quera import Quera
from .usaco import Usaco
from .util.initparser import InitParser

PARSERS = {
    "init": InitParser,
    "atc": AtCoder,
    "atcoder": AtCoder,
    "cf": Codeforces,
    "codeforces": Codeforces,
    "quera": Quera,
    "us": Usaco,
    "usaco": Usaco,
}


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="== [%(levelname)s] %(name)7s: %(message)s")
    logger = logging.getLogger("main")

    usage = "\n  upt [-h]\n" + \
            "\n".join(f"  upt {alias} [-h]" for alias in PARSERS.keys())
    # noinspection PyTypeChecker
    argparser = argparse.ArgumentParser(prog="upt", usage=usage, formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v",
                           "--version",
                           action="version",
                           version=f"{__name__} {__version__}")
    argparser.add_argument("parser",
                           help=argparse.SUPPRESS)
    argparser.add_argument("command",
                           nargs=argparse.REMAINDER,
                           help=argparse.SUPPRESS)

    if len(sys.argv) < 2:
        argparser.print_help()
        sys.exit(0)

    args = argparser.parse_args(sys.argv[1:])

    if args.parser not in PARSERS:
        logger.error(f"No parser named \"{args.parser}\".")
        return

    main_parser = PARSERS.get(args.parser)(alias=args.parser)
    main_parser.parse(args.command)


if __name__ == "__main__":
    main()
