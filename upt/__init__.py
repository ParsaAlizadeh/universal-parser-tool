__version__ = "1.4.1"

import argparse
import logging
import os
import sys

from .atcoder import AtCoder
from .codechef import Codechef
from .codeforces import Codeforces
from .quera import Quera
from .spoj import Spoj
from .util.initparser import InitParser

PARSERS = {
    "init": InitParser,
    "atcoder": AtCoder,
    "codechef": Codechef,
    "cf": Codeforces,
    "quera": Quera,
    "spoj": Spoj,
}


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="== [%(levelname)s] %(name)7s: %(message)s")
    logger = logging.getLogger("main")

    usage = "\n  upt [-h]\n" + \
            "\n".join("  " + parser.usage for parser in PARSERS.values())
    argparser = argparse.ArgumentParser(prog="upt",
                                        usage=usage,
                                        formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v",
                           "--version",
                           action="version",
                           version=__version__)
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
        logger.warning(f"No parser named \"{args.parser}\", try running cf...")
        os.system("cf " + " ".join(sys.argv[1:]))
        return

    main_parser = PARSERS.get(args.parser)()
    main_parser.parse(args.command)


if __name__ == "__main__":
    main()
