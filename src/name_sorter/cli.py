import argparse
import io
import sys
from collections.abc import Sequence
from pathlib import Path

from name_sorter.person_name import InvalidNameError
from name_sorter.readers import NameFileReader
from name_sorter.sort_order import sort_by_last_name_then_given_names
from name_sorter.sorter import NameSorter
from name_sorter.writers import ConsoleNameWriter, NameFileWriter

SORTED_NAMES_FILE = Path("sorted-names-list.txt")


def main(argv: Sequence[str] | None = None) -> int:
    names_file = _parse_arguments(argv).names_file
    _print_in_utf8()
    sorter = NameSorter(
        reader=NameFileReader(names_file),
        sort_names=sort_by_last_name_then_given_names,
        writers=[ConsoleNameWriter(sys.stdout), NameFileWriter(SORTED_NAMES_FILE)],
    )
    try:
        sorter.run()
    except (OSError, InvalidNameError) as error:
        _print_error(str(error))
        return 1
    except UnicodeDecodeError:
        _print_error(f"{names_file} is not a UTF-8 or UTF-16 text file")
        return 1
    return 0


def _parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="name-sorter",
        description=(
            "Sort names by last name, then by given names. Prints the sorted names and "
            "saves them to sorted-names-list.txt in the current directory."
        ),
    )
    parser.add_argument("names_file", type=Path, help="text file with one name per line")
    return parser.parse_args(argv)


def _print_in_utf8() -> None:
    # On Windows, redirected output is encoded with a legacy code page such as cp1252, which
    # has no "Ł", so printing such a name would crash before the file is saved.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")


def _print_error(message: str) -> None:
    print(f"name-sorter: error: {message}", file=sys.stderr)
