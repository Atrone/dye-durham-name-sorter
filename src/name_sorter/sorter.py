"""Coordinates the program's steps: read the names, sort them, and write them out."""

from collections.abc import Callable, Iterable, Sequence

from name_sorter.person_name import PersonName
from name_sorter.readers import NameReader
from name_sorter.writers import NameWriter


class NameSorter:
    """Reads names, sorts them, and gives the sorted names to every writer.

    NameSorter only coordinates. Where the names come from, how they're ordered, and
    where they go are all passed in, so each can be changed or tested on its own.
    """

    def __init__(
        self,
        reader: NameReader,
        sort_names: Callable[[Iterable[PersonName]], list[PersonName]],
        writers: Sequence[NameWriter],
    ) -> None:
        """Create a sorter from the parts that do the actual work.

        Args:
            reader: Supplies the names to sort.
            sort_names: Returns the names in the order they should be written.
            writers: Each one receives all of the sorted names, in the order listed here.
        """
        # Nothing is read or written yet; that happens in run().
        self._reader = reader
        self._sort_names = sort_names
        self._writers = writers

    def run(self) -> None:
        """Read the names, sort them, and pass the result to each writer.

        Every name is read and checked before anything is written, so invalid input
        never leaves partial output behind.
        """
        # read_names() raises on the first invalid name, before any writer has run.
        names = self._reader.read_names()
        sorted_names = self._sort_names(names)
        # Every writer gets the same list: in the program, one prints it and one saves it.
        for writer in self._writers:
            writer.write_names(sorted_names)
