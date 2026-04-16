"""Demo entry point: ``python3 -m diffable`` from a directory containing eGPIO.json / eRST.json."""

from pathlib import Path

from .core import DiffTable

if __name__ == "__main__":
    cwd = Path.cwd()
    demos = [
        ("eGPIO.json", "eGPIO Register Map"),
        ("eRST.json", "eRST Register Map"),
    ]
    for filename, title in demos:
        path = cwd / filename
        if path.exists():
            DiffTable(path, title=title, key="index").generate()
