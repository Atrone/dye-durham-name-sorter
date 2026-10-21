"""The order names are sorted in: by last name, then by given names."""

from collections.abc import Iterable

from name_sorter.person_name import PersonName


def sort_by_last_name_then_given_names(names: Iterable[PersonName]) -> list[PersonName]:
    """Return the names sorted by last name, then by each given name in turn.

    Letter case is ignored, so "Dean" sorts before "DeLuca", as in a phone book. When one
    person's given names match the start of another's, the person with fewer given names
    comes first: "Leo Gardner" sorts before "Leo Ethan Gardner". Names that compare as
    equal, such as "Leo Gardner" and "leo gardner", stay in their original order.
    """
    # sorted() is stable, which is what keeps names that compare as equal in their original order.
    return sorted(names, key=_sort_key)


def _sort_key(name: PersonName) -> tuple[str, tuple[str, ...]]:
    """Return what a name is compared by: its last name, then its given names in order."""
    # casefold() is Python's recommended way to compare text while ignoring letter case.
    last_name = name.last_name.casefold()
    # Tuples compare item by item, and a shorter tuple sorts first when it matches the start
    # of a longer one, which is exactly the given-name rule described above.
    given_names = tuple(given_name.casefold() for given_name in name.given_names)
    return (last_name, given_names)
