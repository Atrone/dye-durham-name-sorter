import io
from pathlib import Path

from name_sorter.person_name import PersonName
from name_sorter.writers import ConsoleNameWriter, NameFileWriter

NAMES = [PersonName.parse("Marin Alvarez"), PersonName.parse("Adonis Julius Archer")]


def test_console_writer_prints_one_name_per_line() -> None:
    console = io.StringIO()

    ConsoleNameWriter(console).write_names(NAMES)

    assert console.getvalue() == "Marin Alvarez\nAdonis Julius Archer\n"


def test_file_writer_saves_one_name_per_line(tmp_path: Path) -> None:
    output_file = tmp_path / "sorted-names-list.txt"

    NameFileWriter(output_file).write_names(NAMES)

    assert output_file.read_text(encoding="utf-8") == "Marin Alvarez\nAdonis Julius Archer\n"


def test_file_writer_replaces_an_existing_file(tmp_path: Path) -> None:
    # The old content is longer than the new, so any leftover lines would show up.
    output_file = tmp_path / "sorted-names-list.txt"
    output_file.write_text("Old Name\nAnother Old Name\nYet Another Old Name\n", encoding="utf-8")

    NameFileWriter(output_file).write_names(NAMES)

    assert output_file.read_text(encoding="utf-8") == "Marin Alvarez\nAdonis Julius Archer\n"
