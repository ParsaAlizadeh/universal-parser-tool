__version__ = "3.2.0"

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
        format="== [%(levelname)s] %(name)7s: %(message)s"
    )
    logger = logging.getLogger("main")

    usage = "\n  %(prog)s [-h]\n" + \
            "\n".join(f"  %(prog)s {alias} [-h]" for alias in PARSERS)
    # noinspection PyTypeChecker
    argparser = argparse.ArgumentParser(
        prog='upt',
        usage=usage,
        formatter_class=argparse.RawTextHelpFormatter
    )
    argparser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s-{__version__}"
    )
    argparser.add_argument(
        "parser",
        help=argparse.SUPPRESS
    )
    argparser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help=argparse.SUPPRESS
    )

    if len(sys.argv) < 2:
        argparser.print_help()
        sys.exit(0)

    args = argparser.parse_args()

    if args.parser not in PARSERS:
        logger.error('No parser named "%s".', args.parser)
        return

    main_parser = PARSERS.get(args.parser)(alias=args.parser)
    main_parser.parse(args.command)


if __name__ == "__main__":
    main()
