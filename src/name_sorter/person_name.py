from dataclasses import dataclass
from typing import Self

MIN_GIVEN_NAMES = 1
MAX_GIVEN_NAMES = 3


class InvalidNameError(ValueError):
    pass


@dataclass(frozen=True)
class PersonName:
    given_names: tuple[str, ...]
    last_name: str

    def __post_init__(self) -> None:
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
        words = text.split()
        if not words:
            raise InvalidNameError("a name can't be blank")
        *given_names, last_name = words
        return cls(given_names=tuple(given_names), last_name=last_name)

    @property
    def full_name(self) -> str:
        return " ".join((*self.given_names, self.last_name))


def _is_single_word(text: str) -> bool:
    return text != "" and not any(character.isspace() for character in text)
