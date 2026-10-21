from collections.abc import Callable, Iterable, Sequence

from name_sorter.person_name import PersonName
from name_sorter.readers import NameReader
from name_sorter.writers import NameWriter


class NameSorter:
    def __init__(
        self,
        reader: NameReader,
        sort_names: Callable[[Iterable[PersonName]], list[PersonName]],
        writers: Sequence[NameWriter],
    ) -> None:
        self._reader = reader
        self._sort_names = sort_names
        self._writers = writers

    def run(self) -> None:
        names = self._reader.read_names()
        sorted_names = self._sort_names(names)
        for writer in self._writers:
            writer.write_names(sorted_names)
