import pytest

from name_sorter.person_name import InvalidNameError, PersonName


@pytest.mark.parametrize(
    ("text", "given_names", "last_name"),
    [
        ("Marin Alvarez", ("Marin",), "Alvarez"),
        ("Adonis Julius Archer", ("Adonis", "Julius"), "Archer"),
        ("Hunter Uriah Mathew Clarke", ("Hunter", "Uriah", "Mathew"), "Clarke"),
    ],
)
def test_parse_treats_the_last_word_as_the_last_name(
    text: str, given_names: tuple[str, ...], last_name: str
) -> None:
    name = PersonName.parse(text)

    assert name.given_names == given_names
    assert name.last_name == last_name


def test_parse_ignores_extra_whitespace() -> None:
    name = PersonName.parse("  Hunter \t Uriah   Clarke \n")

    assert name == PersonName(given_names=("Hunter", "Uriah"), last_name="Clarke")


def test_parse_keeps_hyphens_and_apostrophes_inside_words() -> None:
    name = PersonName.parse("Mary-Jane O'Brien")

    assert name == PersonName(given_names=("Mary-Jane",), last_name="O'Brien")


@pytest.mark.parametrize("text", ["", "   ", "\t"])
def test_parse_rejects_blank_text(text: str) -> None:
    with pytest.raises(InvalidNameError, match="blank"):
        PersonName.parse(text)


def test_parse_rejects_a_name_with_no_given_name() -> None:
    with pytest.raises(InvalidNameError, match="1 to 3 given names"):
        PersonName.parse("Madonna")


def test_parse_rejects_more_than_three_given_names() -> None:
    with pytest.raises(InvalidNameError, match="1 to 3 given names"):
        PersonName.parse("Hunter Uriah Mathew James Clarke")


def test_full_name_puts_the_given_names_before_the_last_name() -> None:
    name = PersonName(given_names=("Adonis", "Julius"), last_name="Archer")

    assert name.full_name == "Adonis Julius Archer"


@pytest.mark.parametrize("given_names", [(), ("Hunter", "Uriah", "Mathew", "James")])
def test_constructor_enforces_the_number_of_given_names(given_names: tuple[str, ...]) -> None:
    with pytest.raises(InvalidNameError, match="1 to 3 given names"):
        PersonName(given_names=given_names, last_name="Clarke")


@pytest.mark.parametrize(
    ("given_names", "last_name"),
    [
        (("",), "Gardner"),
        (("Leo Ethan",), "Gardner"),
        (("Leo",), ""),
        (("Leo",), " Gardner"),
    ],
)
def test_constructor_rejects_parts_that_are_not_single_words(
    given_names: tuple[str, ...], last_name: str
) -> None:
    with pytest.raises(InvalidNameError, match="one word"):
        PersonName(given_names=given_names, last_name=last_name)
