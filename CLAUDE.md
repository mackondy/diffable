# Diffable

Interactive HTML diff viewer for versioned spreadsheet/JSON data. Generates self-contained HTML pages that visualize row-level and cell-level changes across versions.

## Architecture

A single package, no framework:

- `diffable/core.py` — All Python logic: `DiffTable` (JSON→HTML), `SpreadsheetConverter` (xlsx/csv→JSON), `ExcelDiff` and `ZipDiff` (batch directory pipelines)
- `diffable/_templates.py` — `string.Template` constants: `STYLE` (CSS), `JS_TEMPLATE` (all client-side logic), `HTML_TEMPLATE` (page structure)
- `diffable/__init__.py` — public API re-exports
- `diffable/__main__.py` — demo entry point for `python3 -m diffable`

Output is a single self-contained HTML file (no external dependencies). All diff logic runs client-side in JavaScript embedded via the templates.

## Key concepts

- **Versioned JSON format**: `{"versions": [{"version": "v1.0", "date": "...", "<data_key>": [...rows]}]}`
- **Row identity**: Determined by `key` field (defaults to first column). Rows with null/empty key are spacer rows.
- **Diff statuses**: added, removed, modified, unchanged — computed by comparing current vs previous version
- **Inline diff**: Word-level LCS diff highlights exactly which words changed within modified cells (`.hi` spans inside `.diff-old`/`.diff-new`)

## Running

```bash
pip install -e .                       # editable install (add [xlsx] for openpyxl extra)
python3 -m diffable                    # generates HTML from eGPIO.json / eRST.json in cwd
python3 -c "from diffable import DiffTable; DiffTable('file.json', title='Title', key='id').generate()"
```

Optional dependency: `openpyxl` (only needed for xlsx input) — install via `pip install -e .[xlsx]`.

## Common tasks

- **Modify diff rendering**: Edit `JS_TEMPLATE` in `diffable/_templates.py`, specifically `renderTable()` for table logic and `inlineDiff()` for word-level highlighting
- **Change styling**: Edit `STYLE` in `diffable/_templates.py`
- **Change side panel behavior**: Edit `showDetails()` in `JS_TEMPLATE`
- **Add new input formats**: Add methods to `SpreadsheetConverter` in `diffable/core.py`

## Notes

- HTML and JSON files are gitignored (they're generated output)
- Templates use `string.Template` (`$VAR` substitution), not Jinja — dollar signs in JS must be escaped as `$$`
- The `esc()` JS function handles HTML escaping for security
