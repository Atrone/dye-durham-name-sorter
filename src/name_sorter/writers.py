"""Where sorted names go: the NameWriter interface, and writers for the console and files."""

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, TextIO

from name_sorter.person_name import PersonName


class NameWriter(Protocol):
    """Anything that can receive the sorted names, such as the console or a file."""

    def write_names(self, names: Sequence[PersonName]) -> None:
        """Write out the names in the order given."""
        # A Protocol only describes the method; each writer provides its own body.
        ...


class ConsoleNameWriter:
    """Prints names to the console, one per line."""

    def __init__(self, console: TextIO) -> None:
        """Create a writer that prints to console, which is normally sys.stdout."""
        # Taking the stream as a parameter, instead of using sys.stdout here, lets tests read it.
        self._console = console

    def write_names(self, names: Sequence[PersonName]) -> None:
        """Print each name on its own line."""
        for name in names:
            # print() ends each name with a newline.
            print(name.full_name, file=self._console)


class NameFileWriter:
    """Saves names to a text file, one per line, replacing the file if it already exists."""

    def __init__(self, path: Path) -> None:
        """Create a writer for path. A relative path is relative to the working directory."""
        # The file isn't created or touched until write_names runs.
        self._path = path

    def write_names(self, names: Sequence[PersonName]) -> None:
        """Save the names to the file, one per line, replacing anything already in it."""
        # Mode "w" empties an existing file first. UTF-8 keeps accented names intact on every OS.
        with self._path.open("w", encoding="utf-8") as file:
            for name in names:
                # Every line ends with a newline, including the last, as text files normally do.
                file.write(f"{name.full_name}\n")
