import argparse
import importlib
import pkgutil
import logging
import sys
from typing import Mapping

from . import __version__
from .initparser import InitParser
from .baseparser import BaseParser

logger = logging.getLogger("main")


def detect_parsers() -> Mapping[str, type]:
    result = {'init': InitParser}
    plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name[:4] == "upt-"
    }
    for plugin_name, plugin_mod in plugins.items():
        try:
            plugin_parsers = plugin_mod.register()
            result.update(plugin_parsers)
        except AttributeError:
            logger.warning("Plugin %s failed to register", plugin_name)
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
    alias = args.parser

    if alias not in parsers:
        logger.error('No parser named "%s".', alias)
        return

    mod_type = parsers.get(alias)
    mod: BaseParser = mod_type(alias=alias)
    mod.run(args.command)


if __name__ == "__main__":
    main()
