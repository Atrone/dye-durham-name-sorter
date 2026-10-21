from name_sorter.person_name import PersonName
from name_sorter.sort_order import sort_by_last_name_then_given_names


def _sort(*full_names: str) -> list[str]:
    names = [PersonName.parse(full_name) for full_name in full_names]
    return [name.full_name for name in sort_by_last_name_then_given_names(names)]


def test_sorts_by_last_name_first() -> None:
    assert _sort("Adam Zimmer", "Zoe Adams") == ["Zoe Adams", "Adam Zimmer"]


def test_sorts_people_with_the_same_last_name_by_their_first_given_name() -> None:
    assert _sort("Leo Adam Gardner", "Ava Zane Gardner") == [
        "Ava Zane Gardner",
        "Leo Adam Gardner",
    ]


def test_moves_on_to_later_given_names_when_earlier_ones_match() -> None:
    assert _sort("Leo Ethan Gardner", "Leo Adam Gardner") == [
        "Leo Adam Gardner",
        "Leo Ethan Gardner",
    ]
    assert _sort("Leo Adam Zane Gardner", "Leo Adam Bo Gardner") == [
        "Leo Adam Bo Gardner",
        "Leo Adam Zane Gardner",
    ]


def test_puts_fewer_given_names_first_when_the_others_match() -> None:
    assert _sort("Leo Ethan Gardner", "Leo Gardner") == ["Leo Gardner", "Leo Ethan Gardner"]


def test_ignores_letter_case() -> None:
    # Comparing raw characters would put "DeLuca" first, because "L" sorts before "a".
    assert _sort("Ann DeLuca", "Ann Dean") == ["Ann Dean", "Ann DeLuca"]


def test_keeps_duplicate_names() -> None:
    assert _sort("Leo Gardner", "Ava Gardner", "Leo Gardner") == [
        "Ava Gardner",
        "Leo Gardner",
        "Leo Gardner",
    ]


def test_keeps_names_that_differ_only_in_case_in_their_original_order() -> None:
    assert _sort("leo gardner", "Leo Gardner") == ["leo gardner", "Leo Gardner"]
    assert _sort("Leo Gardner", "leo gardner") == ["Leo Gardner", "leo gardner"]
