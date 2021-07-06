import argparse
import importlib
import inspect
import logging
import sys
from typing import Dict

from . import __version__
from .baseparser import BaseParser
from .initparser import InitParser

logger = logging.getLogger("main")


def detect_parsers() -> Dict[str, BaseParser]:
    result = {
        'init': InitParser('init')
    }
    service_mod = importlib.import_module('.services', __package__)
    for _, klass in inspect.getmembers(service_mod, inspect.isclass):
        if not issubclass(klass, BaseParser):
            continue
        dummy: BaseParser = klass(alias=None)
        for alias in dummy.aliases:
            if alias in result:
                logger.warning('Multiple aliases for %s', alias)
                continue
            result[alias] = klass(alias)
    return result


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="== [%(levelname)s] %(name)7s: %(message)s"
    )

    parsers = detect_parsers()
    usage = (
        "\n  %(prog)s [-h]\n" +
        "\n".join(f"  %(prog)s {alias} [-h]" for alias in parsers)
    )

    argparser = argparse.ArgumentParser(
        prog='upt',
        usage=usage,
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

    if args.parser not in parsers:
        logger.error('No parser named "%s".', args.parser)
        return

    main_parser = parsers.get(args.parser)
    main_parser.run(args.command)


if __name__ == "__main__":
    main()
