from abc import ABC, abstractmethod
import argparse
from typing import List, Tuple

class BaseParser(ABC):
    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    @abstractmethod
    def aliases(self) -> Tuple[str]:
        ...

    def __init__(self, alias=None):
        self._alias = alias
        self._argparser = argparse.ArgumentParser(
            prog=f'upt {alias}',
            description=self.description
        )

    def run(self, args: List[str]) -> None:
        args = self._argparser.parse_args(args)
        return self.parse(args)

    @abstractmethod
    def parse(self, args: argparse.Namespace) -> None:
        ...
