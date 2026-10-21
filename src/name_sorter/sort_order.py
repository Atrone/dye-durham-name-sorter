from collections.abc import Iterable

from name_sorter.person_name import PersonName


def sort_by_last_name_then_given_names(names: Iterable[PersonName]) -> list[PersonName]:
    return sorted(names, key=_sort_key)


def _sort_key(name: PersonName) -> tuple[str, tuple[str, ...]]:
    last_name = name.last_name.casefold()
    given_names = tuple(given_name.casefold() for given_name in name.given_names)
    return (last_name, given_names)
