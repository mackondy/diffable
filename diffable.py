"""
diffable — Generate interactive HTML diffs from versioned JSON data.

Usage:
    from diffable import DiffTable
    DiffTable("eGPIO.json", title="eGPIO Register Map", key="index").generate()

JSON format:
    {
      "versions": [
        {
          "version": "v1.0",
          "date": "June 2025",
          "<data_key>": [
            {"index": 0, "signal": "SIG_A", "note": "some note", ...}
          ]
        },
        ...
      ]
    }

The library auto-detects the data array key (any key that is not "version" or "date").
The "note" field, if present, is shown in the right-side detail panel.
"""

import csv
import json
from pathlib import Path

_META_KEYS = {"version", "date"}


def _detect_data_key(version_obj):
    """Find the first key in a version object that holds the data array."""
    for k, v in version_obj.items():
        if k not in _META_KEYS and isinstance(v, list):
            return k
    raise ValueError(
        "Could not detect data key. Each version must contain an array field "
        "besides 'version' and 'date'."
    )


def _detect_columns(versions, data_key):
    """Collect all field names across every row in every version, preserving order."""
    seen = {}
    order = 0
    for ver in versions:
        for row in ver.get(data_key, []):
            for k in row:
                if k not in seen:
                    seen[k] = order
                    order += 1
    return [k for k, _ in sorted(seen.items(), key=lambda x: x[1])]


_STYLE = """
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #f5f5f7;
            color: #1d1d1f;
            -webkit-font-smoothing: antialiased;
        }

        .layout { display: flex; height: 100vh; }

        .main-content {
            flex: 1;
            overflow-y: auto;
            padding: 48px 40px;
            transition: margin-right 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        .main-content.panel-open { margin-right: 420px; }

        .header-bar {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 32px;
            flex-wrap: wrap;
            gap: 16px;
        }

        h1 {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #1d1d1f;
            margin-bottom: 6px;
        }

        .subtitle { font-size: 14px; color: #86868b; font-weight: 400; }

        .controls {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .version-control {
            display: flex;
            align-items: center;
            background: #fff;
            padding: 8px 16px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }

        .toggle-control {
            display: flex;
            align-items: center;
            background: #fff;
            padding: 8px 16px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            gap: 10px;
        }
        .toggle-control label {
            font-size: 12px;
            font-weight: 600;
            color: #86868b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            user-select: none;
            cursor: pointer;
        }

        .ios-toggle {
            position: relative;
            width: 44px; height: 26px;
            background: #e8e8ed;
            border-radius: 13px;
            border: none;
            cursor: pointer;
            transition: background 0.3s ease;
            padding: 0;
            flex-shrink: 0;
        }
        .ios-toggle::after {
            content: '';
            position: absolute;
            top: 2px; left: 2px;
            width: 22px; height: 22px;
            background: #fff;
            border-radius: 50%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
            transition: transform 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        .ios-toggle.active {
            background: #34c759;
        }
        .ios-toggle.active::after {
            transform: translateX(18px);
        }
        .ios-toggle:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .version-control label {
            font-size: 12px;
            font-weight: 600;
            color: #86868b;
            margin-right: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .version-select {
            border: 1px solid #e8e8ed;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 14px;
            font-weight: 500;
            color: #1d1d1f;
            background: #fbfbfd;
            cursor: pointer;
            outline: none;
            transition: all 0.2s;
        }
        .version-select:focus, .version-select:hover {
            border-color: #0071e3;
            box-shadow: 0 0 0 3px rgba(0,113,227,0.1);
        }

        .legend {
            display: flex;
            gap: 16px;
            font-size: 12px;
            margin-bottom: 16px;
            color: #86868b;
            font-weight: 500;
        }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .legend-color { width: 12px; height: 12px; border-radius: 3px; border: 1px solid rgba(0,0,0,0.1); }

        table {
            width: 100%;
            min-width: 600px;
            border-collapse: separate;
            border-spacing: 0;
            margin-bottom: 32px;
            background: #fff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }

        thead th {
            background: #eaeaef;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #1d1d1f;
            padding: 14px 16px;
            text-align: left;
            border-bottom: 2px solid #d2d2d7;
            white-space: nowrap;
        }
        thead th:first-child { border-right: 1px solid #d2d2d7; }

        tbody th {
            font-size: 13px;
            font-weight: 600;
            color: #49494d;
            background-color: rgba(0,0,0,0.02);
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #f0f0f5;
            border-right: 1px solid #e8e8ed;
        }

        td {
            padding: 12px 16px;
            font-size: 14px;
            color: #1d1d1f;
            border-bottom: 1px solid #f0f0f5;
        }

        tr:last-child th, tr:last-child td { border-bottom: none; }

        tbody tr { cursor: pointer; transition: background-color 0.15s ease; }
        tbody tr.spacer-row { cursor: default; }

        .fade-in { animation: fadeIn 0.3s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        tbody tr:nth-child(even):not(.diff-added):not(.diff-removed):not(.diff-modified) { background-color: #fafafa; }
        tbody tr:hover:not(.diff-removed):not(.spacer-row) { background-color: #f0f0f5; }
        tbody tr.active { background-color: #e8f0fe !important; }

        .diff-added { background-color: #e6ffed !important; }
        .diff-added:hover { background-color: #d2fbe0 !important; }

        .diff-removed { background-color: #ffeef0 !important; color: #a40e26 !important; cursor: not-allowed; }
        .diff-removed td, .diff-removed th { color: #a40e26 !important; text-decoration: line-through; }

        .diff-modified { background-color: #fff8c5 !important; }
        .diff-modified:hover { background-color: #fcf1a5 !important; }

        .diff-old { color: #d73a49; text-decoration: line-through; margin-right: 6px; font-size: 0.9em; opacity: 0.8; }
        .diff-new { color: #22863a; font-weight: 600; }

        /* --- Side panel --- */
        .detail-panel {
            position: fixed;
            top: 0; right: -420px;
            width: 420px; height: 100vh;
            background: #fff;
            border-left: 1px solid #e8e8ed;
            overflow-y: auto;
            transition: right 0.35s cubic-bezier(0.25,0.1,0.25,1);
            z-index: 100;
            box-shadow: -2px 0 12px rgba(0,0,0,0.06);
        }
        .detail-panel.open { right: 0; }

        .panel-header {
            position: sticky; top: 0;
            background: rgba(255,255,255,0.92);
            backdrop-filter: saturate(180%) blur(20px);
            -webkit-backdrop-filter: saturate(180%) blur(20px);
            padding: 20px 24px 16px;
            border-bottom: 1px solid #e8e8ed;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
        }
        .panel-title { font-size: 17px; font-weight: 600; color: #1d1d1f; }

        .panel-close {
            width: 28px; height: 28px;
            border-radius: 50%;
            background: #e8e8ed; border: none;
            cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px; color: #86868b;
            transition: background 0.15s ease;
        }
        .panel-close:hover { background: #d2d2d7; color: #1d1d1f; }

        .panel-body { padding: 24px; }
        .detail-section { margin-bottom: 24px; }
        .detail-label {
            font-size: 11px; font-weight: 600;
            text-transform: uppercase; letter-spacing: 0.6px;
            color: #86868b; margin-bottom: 6px;
        }
        .detail-value { font-size: 15px; color: #1d1d1f; line-height: 1.5; }

        .note-block {
            background: #f5f5f7;
            border-left: 3px solid #0071e3;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            font-size: 14px;
            line-height: 1.6;
            color: #1d1d1f;
        }

        .placeholder {
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            height: calc(100vh - 80px);
            color: #d2d2d7;
        }
        .placeholder-icon { font-size: 48px; margin-bottom: 12px; }
        .placeholder-text { font-size: 15px; color: #86868b; }
"""


class DiffTable:
    """Generate an interactive, version-diffing HTML page from a JSON file.

    Parameters
    ----------
    json_source : str or Path
        Path to the JSON file.
    title : str
        Page / header title.
    key : str
        The field used to match rows across versions (e.g. "index").
        Defaults to the first field in the data.
    output : str or Path or None
        Output HTML path. Defaults to ``<title>.html`` next to the JSON file.
    columns : list[str] or None
        Explicit column list to display. If None, auto-detected from data.
        The ``key`` column is always shown first as a row header.
    note_field : str
        Field name that holds the note shown in the side panel. Default "note".
    """

    def __init__(self, json_source, *, title="Diff Explorer", key=None,
                 output=None, columns=None, note_field="note"):
        self.json_source = Path(json_source)
        self.title = title
        self._key = key
        self._output = Path(output) if output else None
        self._columns = columns
        self.note_field = note_field

    def generate(self):
        with self.json_source.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if "versions" not in data or not data["versions"]:
            raise ValueError("JSON must contain a non-empty 'versions' array.")

        versions = data["versions"]
        data_key = _detect_data_key(versions[0])
        all_cols = _detect_columns(versions, data_key)

        key = self._key or all_cols[0]
        if key not in all_cols:
            raise ValueError(f"Key field '{key}' not found in data.")

        if self._columns:
            display_cols = [c for c in self._columns if c in all_cols]
        else:
            display_cols = [c for c in all_cols if c != self.note_field]

        # Ensure key is first
        if key in display_cols:
            display_cols.remove(key)
        display_cols.insert(0, key)

        out_path = self._output or (self.json_source.parent / f"{self.title}.html")
        html = self._render(versions, data_key, key, display_cols)
        out_path.write_text(html, encoding="utf-8")
        return out_path

    # --------------------------------------------------------------------- #

    def _render(self, versions, data_key, key, display_cols):
        col_headers = "".join(
            f"<th>{self._col_label(c)}</th>" for c in display_cols
        )
        versions_json = json.dumps(versions)
        display_cols_json = json.dumps(display_cols)
        non_key_cols = [c for c in display_cols if c != key]

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(self.title)}</title>
<style>{_STYLE}</style>
</head>
<body>
<div class="layout">
    <div class="main-content" id="main-content">
        <div class="header-bar">
            <div>
                <h1>{_esc(self.title)}</h1>
                <p class="subtitle">Click any row for details. Switch versions to track changes.</p>
            </div>
            <div class="controls">
                <div class="toggle-control">
                    <label for="changes-toggle">Changes only</label>
                    <button class="ios-toggle" id="changes-toggle" onclick="toggleChangesOnly()" disabled aria-label="Show changes only"></button>
                </div>
                <div class="version-control">
                    <label for="v-select">Version</label>
                    <select id="v-select" class="version-select" onchange="switchVersion(this.value)"></select>
                </div>
            </div>
        </div>

        <div class="legend">
            <div class="legend-item"><div class="legend-color" style="background:#e6ffed;"></div> Added</div>
            <div class="legend-item"><div class="legend-color" style="background:#ffeef0;"></div> Removed</div>
            <div class="legend-item"><div class="legend-color" style="background:#fff8c5;"></div> Modified</div>
        </div>

        <table>
            <thead><tr>{col_headers}</tr></thead>
            <tbody id="table-body"></tbody>
        </table>
    </div>

    <div class="detail-panel" id="detail-panel">
        <div class="panel-header">
            <span class="panel-title" id="panel-title">Details</span>
            <button class="panel-close" onclick="closePanel()" aria-label="Close">&times;</button>
        </div>
        <div class="panel-body" id="panel-body">
            <div class="placeholder">
                <div class="placeholder-icon">&#9776;</div>
                <div class="placeholder-text">Select a row to view details</div>
            </div>
        </div>
    </div>
</div>

<script>
(function() {{
    const KEY        = {json.dumps(key)};
    const DATA_KEY   = {json.dumps(data_key)};
    const COLS       = {display_cols_json};
    const NOTE_FIELD = {json.dumps(self.note_field)};
    const VERSIONS   = {versions_json};

    let activeRow = null;
    let changesOnly = false;

    /* --- Changes-only toggle --- */
    const changesToggle = document.getElementById('changes-toggle');
    window.toggleChangesOnly = function() {{
        changesOnly = !changesOnly;
        changesToggle.classList.toggle('active', changesOnly);
        applyChangesFilter();
    }};

    function updateToggleState(vIdx) {{
        const hasPrev = vIdx > 0;
        changesToggle.disabled = !hasPrev;
        if (!hasPrev && changesOnly) {{
            changesOnly = false;
            changesToggle.classList.remove('active');
        }}
    }}

    function applyChangesFilter() {{
        const rows = document.querySelectorAll('#table-body tr');
        rows.forEach(tr => {{
            if (changesOnly) {{
                const isDiff = tr.classList.contains('diff-added')
                    || tr.classList.contains('diff-removed')
                    || tr.classList.contains('diff-modified');
                tr.style.display = isDiff ? '' : 'none';
            }} else {{
                tr.style.display = '';
            }}
        }});
    }}

    /* --- Panel helpers --- */
    function openPanel() {{
        document.getElementById('detail-panel').classList.add('open');
        document.getElementById('main-content').classList.add('panel-open');
    }}
    function closePanel() {{
        document.getElementById('detail-panel').classList.remove('open');
        document.getElementById('main-content').classList.remove('panel-open');
        if (activeRow) {{ activeRow.classList.remove('active'); activeRow = null; }}
    }}
    window.closePanel = closePanel;

    function setActiveRow(tr) {{
        if (!tr || tr.classList.contains('diff-removed')) return;
        if (activeRow) activeRow.classList.remove('active');
        tr.classList.add('active');
        activeRow = tr;
    }}

    /* --- Version dropdown --- */
    const vSelect = document.getElementById('v-select');
    VERSIONS.forEach((v, i) => {{
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = v.version + (v.date ? ' (' + v.date + ')' : '');
        vSelect.appendChild(opt);
    }});
    vSelect.value = VERSIONS.length - 1;

    window.switchVersion = function(idx) {{
        closePanel();
        const vIdx = parseInt(idx);
        updateToggleState(vIdx);
        renderTable(vIdx);
        applyChangesFilter();
        const tbody = document.getElementById('table-body');
        tbody.classList.remove('fade-in');
        void tbody.offsetWidth;
        tbody.classList.add('fade-in');
    }};

    /* --- Escape HTML --- */
    function esc(s) {{
        if (s == null) return '';
        return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }}

    /* --- Diff logic --- */
    function renderTable(vIdx) {{
        const curr = VERSIONS[vIdx];
        const prev = vIdx > 0 ? VERSIONS[vIdx - 1] : null;
        const cData = curr[DATA_KEY] || [];
        const pData = prev ? (prev[DATA_KEY] || []) : [];
        const cMap = new Map(cData.filter(r => r[KEY] != null && r[KEY] !== '').map(r => [r[KEY], r]));
        const pMap = new Map(pData.filter(r => r[KEY] != null && r[KEY] !== '').map(r => [r[KEY], r]));

        // Build ordered list from current version (preserves JSON order, including empty rows)
        const ordered = [];
        const usedKeys = new Set();
        for (const row of cData) {{
            if (row[KEY] == null || row[KEY] === '') {{
                ordered.push(null); // spacer
            }} else {{
                ordered.push(row[KEY]);
                usedKeys.add(row[KEY]);
            }}
        }}
        // Append removed rows (in prev but not in curr) at the end
        for (const pk of pMap.keys()) {{
            if (!usedKeys.has(pk)) ordered.push(pk);
        }}

        let html = '';

        for (const k of ordered) {{
            if (k === null) {{
                html += '<tr class="spacer-row"><th></th>'
                    + '<td colspan="' + (COLS.length - 1) + '"></td></tr>';
                continue;
            }}

            const c = cMap.get(k);
            const p = pMap.get(k);

            let status = 'unchanged';
            if (!prev) {{
                status = 'unchanged';
            }} else if (c && !p) {{
                status = 'added';
            }} else if (!c && p) {{
                status = 'removed';
            }} else if (c && p) {{
                for (const col of COLS) {{
                    if (String(c[col] ?? '') !== String(p[col] ?? '')) {{ status = 'modified'; break; }}
                }}
                // Also check note field
                if (status === 'unchanged' && String(c[NOTE_FIELD] ?? '') !== String(p[NOTE_FIELD] ?? '')) {{
                    status = 'modified';
                }}
            }}

            const item = c || p;
            let cls = '';
            if (status === 'added')    cls = 'diff-added';
            if (status === 'removed')  cls = 'diff-removed';
            if (status === 'modified') cls = 'diff-modified';

            const rowIdx = ordered.indexOf(k);
            const onclick = status === 'removed'
                ? ''
                : 'onclick="showDetails(' + rowIdx + ', this)"';

            html += '<tr class="' + cls + '" ' + onclick + '>';
            for (let ci = 0; ci < COLS.length; ci++) {{
                const col = COLS[ci];
                const cVal = esc(c ? c[col] : item[col]);
                const pVal = esc(p ? p[col] : '');
                let cell;
                if (status === 'modified' && c && p && String(c[col] ?? '') !== String(p[col] ?? '')) {{
                    cell = '<span class="diff-old">' + pVal + '</span><span class="diff-new">' + cVal + '</span>';
                }} else {{
                    cell = esc(item[col]);
                }}
                if (ci === 0) {{
                    html += '<th>' + cell + '</th>';
                }} else {{
                    html += '<td>' + cell + '</td>';
                }}
            }}
            html += '</tr>';
        }}

        document.getElementById('table-body').innerHTML = html;

        // Store current diff data for panel use
        window._diffState = {{ cMap, pMap, ordered, prev, status: null }};
    }}

    /* --- Side panel details --- */
    window.showDetails = function(rowIdx, tr) {{
        setActiveRow(tr);
        const k = window._diffState.ordered[rowIdx];
        const c = window._diffState.cMap.get(k);
        const p = window._diffState.prev ? window._diffState.pMap.get(k) : null;
        const item = c || p;

        let html = '';

        // Note section
        const note = item[NOTE_FIELD];
        if (note) {{
            let noteHtml;
            const pNote = p ? String(p[NOTE_FIELD] ?? '') : '';
            const cNote = c ? String(c[NOTE_FIELD] ?? '') : '';
            if (p && cNote !== pNote && pNote) {{
                noteHtml = '<div class="detail-section"><div class="detail-label">Note (changed)</div>'
                    + '<div class="note-block" style="border-left-color:#d73a49;opacity:0.7;margin-bottom:8px;text-decoration:line-through">' + esc(pNote) + '</div>'
                    + '<div class="note-block">' + esc(cNote) + '</div></div>';
            }} else {{
                noteHtml = '<div class="detail-section"><div class="detail-label">Note</div>'
                    + '<div class="note-block">' + esc(note) + '</div></div>';
            }}
            html += noteHtml;
        }}

        document.getElementById('panel-title').innerText = String(item[KEY]);
        document.getElementById('panel-body').innerHTML = html;
        openPanel();
    }};

    // Initial render
    window.switchVersion(VERSIONS.length - 1);
}})();
</script>
</body>
</html>"""

    @staticmethod
    def _col_label(name):
        """Turn a field name like 'during' into a readable header."""
        return _esc(name.replace("_", " ").title())


def _esc(s):
    """HTML-escape a string."""
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


class SpreadsheetConverter:
    """Convert xlsx/csv files to the versioned JSON format used by DiffTable.

    Parameters
    ----------
    source : str or Path
        Path to an .xlsx, .xls, or .csv file.
    output_dir : str or Path or None
        Directory for output JSON files. Defaults to the source file's directory.
    version : str
        Version label for this import (e.g. "v1.0").
    date : str or None
        Optional date string (e.g. "April 2026").
    data_key : str
        Key name for the data array in the JSON. Default "data".

    Usage::

        # CSV
        SpreadsheetConverter("pins.csv", version="v1.0").convert()

        # Excel — each sheet becomes its own JSON file
        SpreadsheetConverter("spec.xlsx", version="v2.0").convert()

        # Append a new version to existing JSON files
        SpreadsheetConverter("spec.xlsx", version="v2.1").convert(append=True)
    """

    def __init__(self, source, *, output_dir=None, version="v1.0", date=None,
                 data_key="data"):
        self.source = Path(source)
        self.output_dir = Path(output_dir) if output_dir else self.source.parent
        self.version = version
        self.date = date
        self.data_key = data_key

    def convert(self, append=False):
        """Convert the source file and write JSON files.

        Parameters
        ----------
        append : bool
            If True and the output JSON already exists, append as a new version
            entry instead of overwriting. Default False.

        Returns
        -------
        list[Path]
            Paths of the generated JSON files.
        """
        suffix = self.source.suffix.lower()
        if suffix == ".csv":
            sheets = {"": self._read_csv()}
        elif suffix in (".xlsx", ".xls"):
            sheets = self._read_excel()
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        stem = self.source.stem
        outputs = []
        for sheet_name, rows in sheets.items():
            if sheet_name:
                filename = f"{stem}_{self._safe_name(sheet_name)}.json"
            else:
                filename = f"{stem}.json"
            out_path = self.output_dir / filename

            version_entry = {"version": self.version}
            if self.date:
                version_entry["date"] = self.date
            version_entry[self.data_key] = rows

            if append and out_path.exists():
                with out_path.open("r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing["versions"].append(version_entry)
            else:
                existing = {"versions": [version_entry]}

            with out_path.open("w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)

            outputs.append(out_path)

        return outputs

    def _read_csv(self):
        with self.source.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    def _read_excel(self):
        try:
            import openpyxl
        except ImportError:
            raise ImportError(
                "openpyxl is required for xlsx support. "
                "Install it with: pip install openpyxl"
            )

        wb = openpyxl.load_workbook(self.source, read_only=True, data_only=True)
        sheets = {}
        for name in wb.sheetnames:
            ws = wb[name]
            rows_iter = ws.iter_rows(values_only=True)
            headers = next(rows_iter, None)
            if not headers:
                continue
            headers = [str(h) if h is not None else f"col_{i}"
                       for i, h in enumerate(headers)]
            rows = []
            for row in rows_iter:
                record = {}
                for h, val in zip(headers, row):
                    if val is None:
                        record[h] = ""
                    else:
                        record[h] = val if isinstance(val, (int, float, bool)) else str(val)
                rows.append(record)
            sheets[name] = rows
        wb.close()
        return sheets

    @staticmethod
    def _safe_name(name):
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


if __name__ == "__main__":
    t = DiffTable("eGPIO.json", title="eGPIO Register Map", key="index")
    out = t.generate()
    print(f"Generated: {out}")
