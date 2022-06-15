from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import List


class BaseParser(ABC):
    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    @abstractmethod
    def aliases(self) -> List[str]:
        ...

    def __init__(self, subparser):
        name, *aliases = self.aliases
        self._argparser: ArgumentParser = subparser.add_parser(
            name, aliases=aliases, help=self.description
        )
        self._argparser.set_defaults(func=self.parse)

    @abstractmethod
    def parse(self, args: Namespace) -> None:
        ...
