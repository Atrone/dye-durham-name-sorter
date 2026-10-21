"""Lets the program run as "python -m name_sorter", the same as the name-sorter command."""

from name_sorter.cli import main

if __name__ == "__main__":
    # Pass main()'s result to the operating system as the process exit code.
    raise SystemExit(main())
