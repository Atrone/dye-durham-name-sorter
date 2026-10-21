import codecs
from pathlib import Path
from typing import Protocol

from name_sorter.person_name import InvalidNameError, PersonName


class NameReader(Protocol):
    def read_names(self) -> list[PersonName]: ...


class NameFileReader:
    def __init__(self, path: Path) -> None:
        self._path = path

    def read_names(self) -> list[PersonName]:
        names: list[PersonName] = []
        for line_number, line in enumerate(self._read_lines(), start=1):
            if not line.strip():
                continue
            try:
                names.append(PersonName.parse(line))
            except InvalidNameError as error:
                raise InvalidNameError(f"{self._path}, line {line_number}: {error}") from error
        return names

    def _read_lines(self) -> list[str]:
        content = self._path.read_bytes()
        # Windows PowerShell 5 saves redirected output as UTF-16 with a byte-order mark.
        if content.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
            return content.decode("utf-16").splitlines()
        # "utf-8-sig" reads UTF-8 with or without a byte-order mark.
        return content.decode("utf-8-sig").splitlines()
