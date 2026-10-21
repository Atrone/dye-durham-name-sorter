from collections.abc import Iterable, Sequence
from operator import attrgetter

import pytest

from name_sorter.person_name import InvalidNameError, PersonName
from name_sorter.sorter import NameSorter


class StubReader:
    def __init__(self, *full_names: str) -> None:
        self._names = [PersonName.parse(full_name) for full_name in full_names]

    def read_names(self) -> list[PersonName]:
        return self._names


class FailingReader:
    def read_names(self) -> list[PersonName]:
        raise InvalidNameError("names.txt, line 3: 'Madonna' is not a valid name")


class RecordingWriter:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def write_names(self, names: Sequence[PersonName]) -> None:
        self.calls.append([name.full_name for name in names])


def reverse_alphabetical(names: Iterable[PersonName]) -> list[PersonName]:
    # Deliberately unlike the real order, to show that NameSorter uses the sort it's given.
    return sorted(names, key=attrgetter("full_name"), reverse=True)


def test_gives_every_writer_the_names_in_sorted_order() -> None:
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
    writer = RecordingWriter()
    sorter = NameSorter(reader=FailingReader(), sort_names=reverse_alphabetical, writers=[writer])

    with pytest.raises(InvalidNameError):
        sorter.run()

    assert writer.calls == []
