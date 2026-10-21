"""Tests for PersonName: reading a name from text, and the rules every name must follow."""

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
    """The last word is the last name, and every word before it is a given name."""
    # One example for each allowed number of given names: one, two and three.
    name = PersonName.parse(text)

    assert name.given_names == given_names
    assert name.last_name == last_name


def test_parse_ignores_extra_whitespace() -> None:
    """Leading, trailing and repeated whitespace, including tabs, doesn't end up in the name."""
    # Spacing like this is easy to produce when a list is edited by hand.
    name = PersonName.parse("  Hunter \t Uriah   Clarke \n")

    assert name == PersonName(given_names=("Hunter", "Uriah"), last_name="Clarke")


def test_parse_keeps_hyphens_and_apostrophes_inside_words() -> None:
    """Only whitespace separates words, so hyphenated names and apostrophes stay whole."""
    # A rule like "split on anything that isn't a letter" would break both of these names.
    name = PersonName.parse("Mary-Jane O'Brien")

    assert name == PersonName(given_names=("Mary-Jane",), last_name="O'Brien")


@pytest.mark.parametrize("text", ["", "   ", "\t"])
def test_parse_rejects_blank_text(text: str) -> None:
    """Text with no words in it isn't a name."""
    # pytest.raises fails the test unless the expected error is raised inside the block.
    with pytest.raises(InvalidNameError, match="blank"):
        PersonName.parse(text)


def test_parse_rejects_a_name_with_no_given_name() -> None:
    """A single word would be a last name with no given name, which the rules don't allow."""
    # The message states the rule, so whoever reads it knows how to fix the line.
    with pytest.raises(InvalidNameError, match="1 to 3 given names"):
        PersonName.parse("Madonna")


def test_parse_rejects_more_than_three_given_names() -> None:
    """Four given names is one more than the rules allow."""
    # The brief's longest example name, with one extra given name added.
    with pytest.raises(InvalidNameError, match="1 to 3 given names"):
        PersonName.parse("Hunter Uriah Mathew James Clarke")


def test_full_name_puts_the_given_names_before_the_last_name() -> None:
    """full_name writes the name the usual way round, with single spaces between parts."""
    # The parts are stored separately; full_name is how a name is printed and saved.
    name = PersonName(given_names=("Adonis", "Julius"), last_name="Archer")

    assert name.full_name == "Adonis Julius Archer"


@pytest.mark.parametrize("given_names", [(), ("Hunter", "Uriah", "Mathew", "James")])
def test_constructor_enforces_the_number_of_given_names(given_names: tuple[str, ...]) -> None:
    """The given-name rule applies however a PersonName is created, not only when parsing."""
    # Creating the name directly skips parse(), so the class itself has to enforce the rule.
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
    """Every part must be one word, or the name would read back differently from its full_name."""
    # For example, a given name of "Leo Ethan" would be read back as two given names.
    with pytest.raises(InvalidNameError, match="one word"):
        PersonName(given_names=given_names, last_name=last_name)
