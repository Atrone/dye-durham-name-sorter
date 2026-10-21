"""The name-sorter command: sorts the names in a file, prints them, and saves them."""

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

# A relative path, so the file is saved in whichever directory the command is run from.
SORTED_NAMES_FILE = Path("sorted-names-list.txt")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the name-sorter command.

    Sorts the names in the file given on the command line, prints them, and saves them
    to sorted-names-list.txt in the current working directory, replacing any older copy.

    Args:
        argv: The command-line arguments, without the program name. Defaults to the
            arguments the program was started with.

    Returns:
        The exit code: 0 on success, or 1 if the names couldn't be read or saved.
        Usage mistakes, such as leaving out the file, exit with code 2 instead.
    """
    # argparse prints a usage message and exits by itself if the arguments are wrong.
    names_file = _parse_arguments(argv).names_file
    _print_in_utf8()
    # The one place that decides which concrete reader, sort order and writers to use.
    sorter = NameSorter(
        reader=NameFileReader(names_file),
        sort_names=sort_by_last_name_then_given_names,
        writers=[ConsoleNameWriter(sys.stdout), NameFileWriter(SORTED_NAMES_FILE)],
    )
    try:
        sorter.run()
    except (OSError, InvalidNameError) as error:
        # Problems the user can fix get a one-line message rather than a traceback.
        _print_error(str(error))
        return 1
    except UnicodeDecodeError:
        # The decoding error itself doesn't say which file was at fault, so add that.
        _print_error(f"{names_file} is not a UTF-8 or UTF-16 text file")
        return 1
    return 0


def _parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command-line arguments, which name the file of names to sort."""
    parser = argparse.ArgumentParser(
        prog="name-sorter",
        description=(
            "Sort names by last name, then by given names. Prints the sorted names and "
            "saves them to sorted-names-list.txt in the current directory."
        ),
    )
    # type=Path hands the reader a Path object rather than a plain string.
    parser.add_argument("names_file", type=Path, help="text file with one name per line")
    return parser.parse_args(argv)


def _print_in_utf8() -> None:
    """Make sure any name can be printed, whatever encoding the console defaults to.

    When output is redirected on Windows, Python encodes it with a legacy code page such
    as cp1252, which has no "Ł". Printing such a name would fail before the file is saved.
    """
    # Only a real text stream can be reconfigured; anything else is left as it is.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")


def _print_error(message: str) -> None:
    """Print an error message to standard error."""
    # Standard error keeps messages out of the sorted names if standard output is redirected.
    print(f"name-sorter: error: {message}", file=sys.stderr)
