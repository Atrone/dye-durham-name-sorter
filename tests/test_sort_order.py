"""Tests for the sort order: by last name, then by given names."""

from name_sorter.person_name import PersonName
from name_sorter.sort_order import sort_by_last_name_then_given_names


def _sort(*full_names: str) -> list[str]:
    """Sort names written as plain text, and return them as plain text."""
    # Converting in and out of PersonName here keeps each test down to one readable line.
    names = [PersonName.parse(full_name) for full_name in full_names]
    return [name.full_name for name in sort_by_last_name_then_given_names(names)]


def test_sorts_by_last_name_first() -> None:
    """The last name decides the order, even when the given names would suggest the opposite."""
    # "Zoe" comes after "Adam", but "Adams" comes before "Zimmer", and the last name wins.
    assert _sort("Adam Zimmer", "Zoe Adams") == ["Zoe Adams", "Adam Zimmer"]


def test_sorts_people_with_the_same_last_name_by_their_first_given_name() -> None:
    """When last names match, the first given name decides."""
    # Both people are Gardners, so Ava comes before Leo.
    assert _sort("Leo Gardner", "Ava Gardner") == ["Ava Gardner", "Leo Gardner"]


def test_moves_on_to_later_given_names_when_earlier_ones_match() -> None:
    """When the earlier names match, the second given name decides, then the third."""
    # The first pair differs only in its second given name; the second pair only in its third.
    assert _sort("Leo Ethan Gardner", "Leo Adam Gardner") == [
        "Leo Adam Gardner",
        "Leo Ethan Gardner",
    ]
    assert _sort("Leo Adam Zane Gardner", "Leo Adam Bo Gardner") == [
        "Leo Adam Bo Gardner",
        "Leo Adam Zane Gardner",
    ]


def test_puts_fewer_given_names_first_when_the_others_match() -> None:
    """A name whose given names match the start of another's comes first, like a shorter word."""
    # Nothing follows "Leo" in the first name, so it sorts before "Leo Ethan".
    assert _sort("Leo Ethan Gardner", "Leo Gardner") == ["Leo Gardner", "Leo Ethan Gardner"]


def test_ignores_letter_case() -> None:
    """Capital and lowercase letters sort together, as in a phone book."""
    # Comparing raw characters would put "DeLuca" first, because capital "L" comes before "a".
    assert _sort("Ann DeLuca", "Ann Dean") == ["Ann Dean", "Ann DeLuca"]


def test_keeps_duplicate_names() -> None:
    """Two people can share a name, so sorting never drops a repeated name."""
    # Both Leo Gardners must still be in the result.
    assert _sort("Leo Gardner", "Ava Gardner", "Leo Gardner") == [
        "Ava Gardner",
        "Leo Gardner",
        "Leo Gardner",
    ]


def test_keeps_names_that_differ_only_in_case_in_their_original_order() -> None:
    """Names that compare as equal stay in the order they were given."""
    # Checked both ways round, to show the order comes from the input, not from letter case.
    assert _sort("leo gardner", "Leo Gardner") == ["leo gardner", "Leo Gardner"]
    assert _sort("Leo Gardner", "leo gardner") == ["Leo Gardner", "leo gardner"]
