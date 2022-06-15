import argparse
import importlib
import inspect
import logging
import pkgutil
import sys
from typing import List

from . import __version__
from .baseparser import BaseParser
from .initparser import InitParser

logger = logging.getLogger("main")


def detect_parsers() -> List[type]:
    parsers = [InitParser]

    def error_register(klass):
        if not inspect.isclass(klass):
            return "Passed parser is not a class"
        if not issubclass(klass, BaseParser):
            return "Passed parser is not inherited from BaseParser"
        return None

    def add_register(plugin_name, klass):
        error_message = error_register(klass)
        if error_message:
            logger.warning(
                "%s, skipping %s",
                error_message, plugin_name
            )
        else:
            parsers.append(klass)

    plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name[:4] == "upt-"
    }
    for plugin_name, plugin_mod in plugins.items():
        try:
            plugin_registers = plugin_mod.register()
            for klass in plugin_registers:
                add_register(plugin_name, klass)
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

    argparser = argparse.ArgumentParser(prog='upt')
    argparser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s-{__version__}"
    )

    subparsers = argparser.add_subparsers(dest='subcommand_name')
    parsers = detect_parsers()
    for klass in parsers:
        _ = klass(subparsers)

    if len(sys.argv) < 2:
        argparser.print_help()
        sys.exit(0)

    args = argparser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
