"""Tests for NameFileReader: reading names from a text file."""

from pathlib import Path

import pytest

from name_sorter.person_name import InvalidNameError, PersonName
from name_sorter.readers import NameFileReader


def test_reads_one_name_per_line(tmp_path: Path) -> None:
    """Each line of the file becomes one name, in the same order as the file."""
    # tmp_path is a fresh directory from pytest, so tests never touch real files.
    names_file = tmp_path / "names.txt"
    names_file.write_text("Janet Parsons\nAdonis Julius Archer\n", encoding="utf-8")

    names = NameFileReader(names_file).read_names()

    assert names == [PersonName.parse("Janet Parsons"), PersonName.parse("Adonis Julius Archer")]


def test_skips_blank_lines(tmp_path: Path) -> None:
    """Empty and whitespace-only lines are skipped, rather than reported as invalid names."""
    # Blank lines, including at the start and end, are common in hand-edited files.
    names_file = tmp_path / "names.txt"
    names_file.write_text("\nJanet Parsons\n   \nLeo Gardner\n\n", encoding="utf-8")

    names = NameFileReader(names_file).read_names()

    assert [name.full_name for name in names] == ["Janet Parsons", "Leo Gardner"]


def test_reports_the_line_number_of_an_invalid_name(tmp_path: Path) -> None:
    """Reading stops at an invalid line, and the error says which line it was."""
    # Line 3 has no given name. The blank line 2 still counts toward the line number.
    names_file = tmp_path / "names.txt"
    names_file.write_text("Janet Parsons\n\nMadonna\nLeo Gardner\n", encoding="utf-8")

    with pytest.raises(InvalidNameError, match="line 3"):
        NameFileReader(names_file).read_names()


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16"])
def test_reads_utf8_and_utf16_files(tmp_path: Path, encoding: str) -> None:
    """Files saved as UTF-8, UTF-8 with a byte-order mark, or UTF-16 all read the same."""
    # Python's "utf-16" codec writes a byte-order mark first, as Windows PowerShell 5 does.
    names_file = tmp_path / "names.txt"
    names_file.write_text("Zoë Ångström\n", encoding=encoding)

    names = NameFileReader(names_file).read_names()

    assert [name.full_name for name in names] == ["Zoë Ångström"]
