import argparse
import importlib
import inspect
import logging
import pkgutil
import sys
from typing import Mapping

from . import __version__
from .baseparser import BaseParser
from .initparser import InitParser

logger = logging.getLogger("main")


def detect_parsers() -> Mapping[str, type]:
    parsers = {'init': InitParser}

    def error_register(alias, klass):
        if alias in parsers:
            return "Multiple alias assigned"
        if not inspect.isclass(klass):
            return "Passed parser is not a class"
        if not issubclass(klass, BaseParser):
            return "Passed parser is not inherited from BaseParser"
        return None

    def add_register(plugin_name, alias, klass):
        error_message = error_register(alias, klass)
        if error_message:
            logger.warning(
                "%s, skipping %s.%s",
                error_message, plugin_name, alias
            )
        parsers[alias] = klass

    plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name[:4] == "upt-"
    }
    for plugin_name, plugin_mod in plugins.items():
        try:
            plugin_registers = plugin_mod.register().items()
            for alias, klass in plugin_registers:
                add_register(plugin_name, alias, klass)
        except AttributeError:
            logger.error("Failed to register, skipping plugin %s", plugin_name)
        except:
            logger.fatal("Unexpected error in register, skipping plugin %s", plugin_name)
    return parsers


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
