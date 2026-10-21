"""A person's name: one to three given names followed by a last name."""

from dataclasses import dataclass
from typing import Self

MIN_GIVEN_NAMES = 1
MAX_GIVEN_NAMES = 3


class InvalidNameError(ValueError):
    """Raised when text, or the parts given to PersonName, don't form a valid name."""


@dataclass(frozen=True)
class PersonName:
    """A person's name: one to three given names followed by a last name.

    A PersonName can't be changed after it's created, and it's always valid: creating
    one that breaks the rules raises InvalidNameError. Code that receives a PersonName
    never needs to check it again.
    """

    given_names: tuple[str, ...]
    last_name: str

    def __post_init__(self) -> None:
        """Check the naming rules, whether the name was parsed or built directly.

        Raises:
            InvalidNameError: If there are fewer than one or more than three given names,
                or if any part is empty or contains whitespace.
        """
        # The brief's rule: at least one given name, and no more than three.
        if not MIN_GIVEN_NAMES <= len(self.given_names) <= MAX_GIVEN_NAMES:
            raise InvalidNameError(
                f"{self.full_name!r} is not a valid name: it needs {MIN_GIVEN_NAMES} to "
                f"{MAX_GIVEN_NAMES} given names followed by a last name"
            )
        # Each part must be one word, or full_name would read back as a different name.
        for part in (*self.given_names, self.last_name):
            if not _is_single_word(part):
                raise InvalidNameError(
                    f"{part!r} is not a valid part of a name: it must be one word"
                )

    @classmethod
    def parse(cls, text: str) -> Self:
        """Read a name written as its given names followed by its last name.

        For example, "Adonis Julius Archer" has the given names "Adonis" and "Julius"
        and the last name "Archer". Words may be separated by any amount of whitespace.

        Raises:
            InvalidNameError: If the text isn't one to three given names followed by a
                last name.
        """
        # With no argument, split() breaks on any run of whitespace and ignores it at either end.
        words = text.split()
        # Without this check, unpacking an empty list below would fail with a confusing error.
        if not words:
            raise InvalidNameError("a name can't be blank")
        # The last word is always the last name, and every word before it is a given name.
        *given_names, last_name = words
        return cls(given_names=tuple(given_names), last_name=last_name)

    @property
    def full_name(self) -> str:
        """The name as it's normally written: given names, then last name, with spaces between."""
        # Rebuilt from the parts, so any extra whitespace in the original text is dropped.
        return " ".join((*self.given_names, self.last_name))


def _is_single_word(text: str) -> bool:
    """Tell whether text is exactly one word: not empty, and containing no whitespace."""
    # isspace() catches tabs and non-breaking spaces as well as ordinary spaces.
    return text != "" and not any(character.isspace() for character in text)
