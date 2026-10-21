"""End-to-end tests for the name-sorter command, run against real files in a temporary folder."""

import random
import subprocess
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path

import pytest

from name_sorter.cli import main

# The example from the brief. Its input says "Vaugh Lewis" but its expected output says
# "Vaughn Lewis"; "Vaughn" is used in both lists so that they agree.
BRIEF_UNSORTED_NAMES = [
    "Janet Parsons",
    "Vaughn Lewis",
    "Adonis Julius Archer",
    "Shelby Nathan Yoder",
    "Marin Alvarez",
    "London Lindsey",
    "Beau Tristan Bentley",
    "Leo Gardner",
    "Hunter Uriah Mathew Clarke",
    "Mikayla Lopez",
    "Frankie Conner Ritter",
]
BRIEF_SORTED_NAMES = [
    "Marin Alvarez",
    "Adonis Julius Archer",
    "Beau Tristan Bentley",
    "Hunter Uriah Mathew Clarke",
    "Leo Gardner",
    "Vaughn Lewis",
    "London Lindsey",
    "Mikayla Lopez",
    "Janet Parsons",
    "Frankie Conner Ritter",
    "Shelby Nathan Yoder",
]

# Small pools of names, so that made-up lists share plenty of last names and given names.
GIVEN_NAME_POOL = ["Ava", "Beau", "Hunter", "Janet", "Leo", "Marin", "Shelby", "Uriah"]
LAST_NAME_POOL = ["Alvarez", "Archer", "Bentley", "Clarke", "Gardner", "Lewis", "Lopez", "Yoder"]


@pytest.fixture
def working_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run the test from an empty temporary folder, which is where the output file is saved."""
    # monkeypatch changes back to the original directory when the test finishes.
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_prints_the_sorted_names_and_saves_them_in_the_working_directory(
    working_directory: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The brief's example is printed in sorted order and saved to sorted-names-list.txt."""
    # Run exactly as the brief does: name-sorter ./unsorted-names-list.txt
    _write_lines(working_directory / "unsorted-names-list.txt", BRIEF_UNSORTED_NAMES)

    exit_code = main(["./unsorted-names-list.txt"])

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == BRIEF_SORTED_NAMES
    assert _read_lines(working_directory / "sorted-names-list.txt") == BRIEF_SORTED_NAMES


def test_sorts_a_thousand_names(working_directory: Path) -> None:
    """A thousand names, the size of the assessment's own test, all come out in order."""
    # The names repeat parts often, so every tie-breaking rule gets exercised.
    unsorted_names = _make_up_names(count=1000)
    _write_lines(working_directory / "names.txt", unsorted_names)

    exit_code = main(["names.txt"])

    sorted_names = _read_lines(working_directory / "sorted-names-list.txt")
    assert exit_code == 0
    # The same names, each the same number of times: nothing lost, added or changed.
    assert Counter(sorted_names) == Counter(unsorted_names)
    assert all(_order_of(first) <= _order_of(second) for first, second in pairwise(sorted_names))


def test_reports_an_invalid_name_and_keeps_the_previous_output(
    working_directory: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An invalid line fails the run with its line number, and the old output file survives."""
    # The output of an earlier successful run, which a failed run must not overwrite.
    output_file = working_directory / "sorted-names-list.txt"
    output_file.write_text("Earlier Result\n", encoding="utf-8")
    _write_lines(working_directory / "names.txt", ["Janet Parsons", "Madonna"])

    exit_code = main(["names.txt"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "names.txt, line 2" in captured.err
    assert captured.out == ""
    assert output_file.read_text(encoding="utf-8") == "Earlier Result\n"


def test_reports_a_missing_file(
    working_directory: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A missing input file gives a one-line error and exit code 1, not a traceback."""
    # The working directory is empty, so this file can't exist.
    exit_code = main(["missing.txt"])

    assert exit_code == 1
    assert "missing.txt" in capsys.readouterr().err


def test_reports_a_file_that_is_not_utf8_or_utf16(
    working_directory: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A file in another encoding gives a clear error instead of a decoding traceback."""
    # 0xEB is "ë" in the Windows-1252 encoding, but it's never valid on its own in UTF-8.
    (working_directory / "names.txt").write_bytes(b"Zo\xeb Parsons\n")

    exit_code = main(["names.txt"])

    assert exit_code == 1
    assert "names.txt is not a UTF-8 or UTF-16 text file" in capsys.readouterr().err


def test_requires_the_names_file_argument(capsys: pytest.CaptureFixture[str]) -> None:
    """Leaving out the file prints usage help and exits with argparse's usage-error code, 2."""
    # argparse ends the program by raising SystemExit rather than returning a code.
    with pytest.raises(SystemExit) as exit_info:
        main([])

    assert exit_info.value.code == 2
    assert "usage: name-sorter" in capsys.readouterr().err


def test_runs_as_a_python_module(tmp_path: Path) -> None:
    """Running "python -m name_sorter" works the same as the name-sorter command."""
    # A separate process exercises the package's real entry point, not just main().
    _write_lines(tmp_path / "names.txt", ["Leo Gardner", "Marin Alvarez"])

    result = subprocess.run(
        [sys.executable, "-m", "name_sorter", "names.txt"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.splitlines() == ["Marin Alvarez", "Leo Gardner"]
    assert _read_lines(tmp_path / "sorted-names-list.txt") == ["Marin Alvarez", "Leo Gardner"]


def _write_lines(path: Path, lines: list[str]) -> None:
    """Save lines to a UTF-8 text file, one per line."""
    # A newline after every line, including the last, like a normal text file.
    path.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")


def _read_lines(path: Path) -> list[str]:
    """Return the lines of a UTF-8 text file."""
    # splitlines() handles both Windows and Unix line endings.
    return path.read_text(encoding="utf-8").splitlines()


def _make_up_names(count: int) -> list[str]:
    """Make up names with one to three given names; the same names on every run."""
    # A fixed seed makes the list, and so the test, the same every time it runs.
    generator = random.Random(2026)
    names: list[str] = []
    for _ in range(count):
        given_names = generator.choices(GIVEN_NAME_POOL, k=generator.randint(1, 3))
        names.append(" ".join([*given_names, generator.choice(LAST_NAME_POOL)]))
    return names


def _order_of(full_name: str) -> tuple[str, list[str]]:
    """Restate the sort rule for one name: last name, then given names, ignoring case."""
    # Written independently of sort_order.py, so a mistake there can't hide by being copied here.
    *given_names, last_name = full_name.casefold().split()
    return (last_name, given_names)
