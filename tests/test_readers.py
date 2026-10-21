from pathlib import Path

import pytest

from name_sorter.person_name import InvalidNameError, PersonName
from name_sorter.readers import NameFileReader


def test_reads_one_name_per_line(tmp_path: Path) -> None:
    names_file = tmp_path / "names.txt"
    names_file.write_text("Janet Parsons\nAdonis Julius Archer\n", encoding="utf-8")

    names = NameFileReader(names_file).read_names()

    assert names == [PersonName.parse("Janet Parsons"), PersonName.parse("Adonis Julius Archer")]


def test_skips_blank_lines(tmp_path: Path) -> None:
    names_file = tmp_path / "names.txt"
    names_file.write_text("\nJanet Parsons\n   \nLeo Gardner\n\n", encoding="utf-8")

    names = NameFileReader(names_file).read_names()

    assert [name.full_name for name in names] == ["Janet Parsons", "Leo Gardner"]


def test_reports_the_line_number_of_an_invalid_name(tmp_path: Path) -> None:
    # The blank line still counts, so "Madonna" is on line 3.
    names_file = tmp_path / "names.txt"
    names_file.write_text("Janet Parsons\n\nMadonna\nLeo Gardner\n", encoding="utf-8")

    with pytest.raises(InvalidNameError, match="line 3"):
        NameFileReader(names_file).read_names()


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16"])
def test_reads_utf8_and_utf16_files(tmp_path: Path, encoding: str) -> None:
    names_file = tmp_path / "names.txt"
    names_file.write_text("Zoë Ångström\n", encoding=encoding)

    names = NameFileReader(names_file).read_names()

    assert [name.full_name for name in names] == ["Zoë Ångström"]
