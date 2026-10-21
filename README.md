# Name Sorter

[![CI](https://github.com/Atrone/dye-durham-name-sorter/actions/workflows/ci.yml/badge.svg)](https://github.com/Atrone/dye-durham-name-sorter/actions/workflows/ci.yml)

Sorts a list of names by last name, then by given names. The sorted names are printed to the
screen and saved to `sorted-names-list.txt` in the current directory.

## Run it

You need Python 3.11 or later.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1      # macOS/Linux: source .venv/bin/activate
pip install .
name-sorter ./unsorted-names-list.txt
```

## Input rules

- One name per line: one to three given names, then a last name, separated by spaces.
- The last word is always the last name, so "Ann de Souza" is sorted under "Souza".
- Blank lines are skipped. Duplicate names are kept.
- Sorting ignores letter case. Names that compare as equal stay in their input order.
- The file can be UTF-8 (with or without a byte-order mark) or UTF-16 with a byte-order mark.
- If a line isn't a valid name, nothing is printed or saved. The program reports the file and
  line number and exits with code 1, leaving any existing `sorted-names-list.txt` as it was.

## Develop

```powershell
pip install -e ".[dev]"
pytest                   # unit and end-to-end tests
ruff check .             # lint
ruff format --check .    # formatting
mypy                     # type check
```

GitHub Actions runs all of these on Linux and Windows, with Python 3.11 and 3.14, on every push
to `main` and every pull request.

## Where things are

| File in `src/name_sorter/` | What it does |
| --- | --- |
| `cli.py` | The command: reads the arguments, wires the parts together, reports errors |
| `sorter.py` | `NameSorter`: reads the names, sorts them, gives the result to each writer |
| `person_name.py` | `PersonName`: parses one name and enforces the given-name rule |
| `sort_order.py` | The sort rule: last name, then given names, ignoring case |
| `readers.py` | The `NameReader` interface and `NameFileReader` |
| `writers.py` | The `NameWriter` interface, `ConsoleNameWriter` and `NameFileWriter` |

To add another output, such as a JSON file, write a class with a `write_names` method and add it
to the `writers` list in `cli.py`. Nothing else needs to change.

## A note on the brief

The brief's example input has "Vaugh Lewis", but its expected output has "Vaughn Lewis". The
program never changes names, so `unsorted-names-list.txt` uses "Vaughn" to match the expected
output.
