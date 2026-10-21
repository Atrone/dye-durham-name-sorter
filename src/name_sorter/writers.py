from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, TextIO

from name_sorter.person_name import PersonName


class NameWriter(Protocol):
    def write_names(self, names: Sequence[PersonName]) -> None: ...


class ConsoleNameWriter:
    def __init__(self, console: TextIO) -> None:
        self._console = console

    def write_names(self, names: Sequence[PersonName]) -> None:
        for name in names:
            print(name.full_name, file=self._console)


class NameFileWriter:
    def __init__(self, path: Path) -> None:
        self._path = path

    def write_names(self, names: Sequence[PersonName]) -> None:
        with self._path.open("w", encoding="utf-8") as file:
            for name in names:
                file.write(f"{name.full_name}\n")
