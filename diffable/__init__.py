"""diffable — Interactive HTML diff viewer for versioned spreadsheet/JSON data."""

from .core import DiffTable, SpreadsheetConverter, ExcelDiff, ZipDiff

__all__ = ["DiffTable", "SpreadsheetConverter", "ExcelDiff", "ZipDiff"]
