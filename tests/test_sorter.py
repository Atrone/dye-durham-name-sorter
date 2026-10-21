"""Tests for NameSorter, using simple stand-ins for the reader and writers."""

from collections.abc import Iterable, Sequence
from operator import attrgetter

import pytest

from name_sorter.person_name import InvalidNameError, PersonName
from name_sorter.sorter import NameSorter


class StubReader:
    """Stands in for a real reader by returning names it was given up front."""

    def __init__(self, *full_names: str) -> None:
        """Remember the names to return, written as plain text."""
        # Parsing here lets each test list its names as simple strings.
        self._names = [PersonName.parse(full_name) for full_name in full_names]

    def read_names(self) -> list[PersonName]:
        """Return the names, as a real reader would after reading its source."""
        # A copy, so nothing the sorter does can change this stub's own list.
        return list(self._names)


class FailingReader:
    """Stands in for a reader that finds an invalid name in its source."""

    def read_names(self) -> list[PersonName]:
        """Raise the same kind of error a real reader raises for an invalid line."""
        # NameSorter should let this error through without calling any writer.
        raise InvalidNameError("names.txt, line 3: 'Madonna' is not a valid name")


class RecordingWriter:
    """Stands in for a real writer by remembering every list it was asked to write."""

    def __init__(self) -> None:
        """Start with nothing written."""
        # One entry per call, so tests can also check how many times the writer was used.
        self.calls: list[list[str]] = []

    def write_names(self, names: Sequence[PersonName]) -> None:
        """Record the names as plain text."""
        # Plain text makes the assertions in the tests easy to read.
        self.calls.append([name.full_name for name in names])


def reverse_alphabetical(names: Iterable[PersonName]) -> list[PersonName]:
    """Sort by full name from Z to A: an order that can't be mistaken for the real one."""
    # A deliberately different order proves NameSorter uses the sort it's given.
    return sorted(names, key=attrgetter("full_name"), reverse=True)


def test_gives_every_writer_the_names_in_sorted_order() -> None:
    """Each writer receives the whole list once, in the order the sort function returned."""
    # Two writers, like the real program's console and file writers.
    console, file = RecordingWriter(), RecordingWriter()
    sorter = NameSorter(
        reader=StubReader("Ava Bell", "Cy Adams", "Bo Cole"),
        sort_names=reverse_alphabetical,
        writers=[console, file],
    )

    sorter.run()

    assert console.calls == [["Cy Adams", "Bo Cole", "Ava Bell"]]
    assert file.calls == [["Cy Adams", "Bo Cole", "Ava Bell"]]


def test_writes_nothing_when_reading_fails() -> None:
    """If the input has an invalid name, no writer runs, so no partial output is left behind."""
    # In the real program, this is what keeps an older sorted-names-list.txt intact.
    writer = RecordingWriter()
    sorter = NameSorter(reader=FailingReader(), sort_names=reverse_alphabetical, writers=[writer])

    with pytest.raises(InvalidNameError):
        sorter.run()

    assert writer.calls == []
