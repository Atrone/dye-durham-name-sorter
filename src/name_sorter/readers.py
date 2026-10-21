"""Where names come from: the NameReader interface, and a reader for text files."""

import codecs
from pathlib import Path
from typing import Protocol

from name_sorter.person_name import InvalidNameError, PersonName


class NameReader(Protocol):
    """Anything that can supply the names to sort."""

    def read_names(self) -> list[PersonName]:
        """Return every name from the source, in the order they appear there.

        Raises:
            InvalidNameError: If the source contains something that isn't a valid name.
        """
        # A Protocol only describes the method; each reader provides its own body.
        ...


class NameFileReader:
    """Reads names from a text file that has one name per line."""

    def __init__(self, path: Path) -> None:
        """Create a reader for the file at path. The file isn't opened until read_names runs."""
        # Only the path is kept, so a missing file is reported when reading, not when wiring up.
        self._path = path

    def read_names(self) -> list[PersonName]:
        """Read every name in the file, skipping blank lines.

        Raises:
            OSError: If the file can't be read, for example because it doesn't exist.
            UnicodeDecodeError: If the file isn't UTF-8 or UTF-16 text.
            InvalidNameError: If a line isn't a valid name. The message gives the line number.
        """
        names: list[PersonName] = []
        # Numbering starts at 1 to match the line numbers a text editor shows.
        for line_number, line in enumerate(self._read_lines(), start=1):
            # Blank lines, such as an empty last line, aren't names, but they aren't errors either.
            if not line.strip():
                continue
            try:
                names.append(PersonName.parse(line))
            except InvalidNameError as error:
                # Add the file and line number, so the bad name can be found and fixed.
                raise InvalidNameError(f"{self._path}, line {line_number}: {error}") from error
        return names

    def _read_lines(self) -> list[str]:
        """Return the file's lines, choosing the text encoding from its byte-order mark."""
        content = self._path.read_bytes()
        # Windows PowerShell 5 saves redirected output as UTF-16 with a byte-order mark.
        if content.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
            return content.decode("utf-16").splitlines()
        # Otherwise expect UTF-8. "utf-8-sig" also strips a UTF-8 byte-order mark, if present.
        return content.decode("utf-8-sig").splitlines()
