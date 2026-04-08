"""HTML, CSS, and JS templates for diffable HTML output."""

from string import Template

STYLE = """
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
            align-items: stretch;
            gap: 16px;
        }

        .control-pill {
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0.03);
            padding: 8px 16px;
            border-radius: 12px;
        }
        .control-pill.toggle-control { gap: 10px; }
        .control-pill label {
            font-size: 12px;
            font-weight: 600;
            color: #86868b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .control-pill.toggle-control label {
            user-select: none;
            cursor: pointer;
        }
        .control-pill.version-control label {
            margin-right: 12px;
            flex-shrink: 0;
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
        .ios-toggle.active { background: #34c759; }
        .ios-toggle.active::after { transform: translateX(18px); }
        .ios-toggle:disabled { opacity: 0.4; cursor: not-allowed; }

        .version-select {
            border: 1px solid #e8e8ed;
            border-radius: 8px;
            padding: 8px 32px 8px 14px;
            font-size: 14px;
            font-weight: 500;
            color: #1d1d1f;
            background: #fbfbfd;
            cursor: pointer;
            outline: none;
            transition: all 0.2s;
            appearance: none;
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2386868b' d='M6 8.825a.5.5 0 0 1-.354-.146L2.11 5.143a.5.5 0 1 1 .707-.707L6 7.618l3.182-3.182a.5.5 0 1 1 .707.707L6.354 8.679A.5.5 0 0 1 6 8.825z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 10px center;
        }
        .version-select:focus, .version-select:hover {
            border-color: #0071e3;
            box-shadow: 0 0 0 3px rgba(0,113,227,0.1);
        }

        .status-tag {
            display: inline-block;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding: 4px 10px;
            border-radius: 6px;
        }
        .status-tag.tag-added    { background: #e6ffed; color: #1a7f37; }
        .status-tag.tag-removed  { background: #ffeef0; color: #a40e26; }
        .status-tag.tag-modified { background: #fff8c5; color: #7a6d1a; }

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
            max-width: 180px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        td {
            padding: 12px 16px;
            font-size: 14px;
            color: #1d1d1f;
            border-bottom: 1px solid #f0f0f5;
            max-width: 220px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
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
        .diff-old .hi { background-color: #fdb8c0; border-radius: 2px; padding: 0 1px; }
        .diff-new .hi { background-color: #acf2bd; border-radius: 2px; padding: 0 1px; }

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

JS_TEMPLATE = Template("""
(function() {
    const KEY        = $KEY;
    const DATA_KEY   = $DATA_KEY;
    const COLS       = $COLS;
    const COL_LABELS = $COL_LABELS;
    const NOTE_FIELD = $NOTE_FIELD;
    const VERSIONS   = $VERSIONS;

    let activeRow = null;
    let changesOnly = true;

    /* --- Changes-only toggle --- */
    const changesToggle = document.getElementById('changes-toggle');
    window.toggleChangesOnly = function() {
        changesOnly = !changesOnly;
        changesToggle.classList.toggle('active', changesOnly);
        applyChangesFilter();
    };

    function updateToggleState(vIdx) {
        const hasPrev = vIdx > 0;
        changesToggle.disabled = !hasPrev;
        if (!hasPrev && changesOnly) {
            changesOnly = false;
            changesToggle.classList.remove('active');
        }
    }

    function applyChangesFilter() {
        const rows = document.querySelectorAll('#table-body tr');
        rows.forEach(tr => {
            if (changesOnly) {
                const isDiff = tr.classList.contains('diff-added')
                    || tr.classList.contains('diff-removed')
                    || tr.classList.contains('diff-modified');
                tr.style.display = isDiff ? '' : 'none';
            } else {
                tr.style.display = '';
            }
        });
    }

    /* --- Panel helpers --- */
    function openPanel() {
        document.getElementById('detail-panel').classList.add('open');
        document.getElementById('main-content').classList.add('panel-open');
    }
    function closePanel() {
        document.getElementById('detail-panel').classList.remove('open');
        document.getElementById('main-content').classList.remove('panel-open');
        if (activeRow) { activeRow.classList.remove('active'); activeRow = null; }
    }
    window.closePanel = closePanel;

    function setActiveRow(tr) {
        if (!tr || tr.classList.contains('diff-removed')) return;
        if (activeRow) activeRow.classList.remove('active');
        tr.classList.add('active');
        activeRow = tr;
    }

    /* --- Version dropdown --- */
    const vSelect = document.getElementById('v-select');
    VERSIONS.forEach((v, i) => {
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = v.version + (v.date ? ' (' + v.date + ')' : '');
        vSelect.appendChild(opt);
    });
    vSelect.value = VERSIONS.length - 1;

    window.switchVersion = function(idx) {
        closePanel();
        const vIdx = parseInt(idx);
        updateToggleState(vIdx);
        renderTable(vIdx);
        applyChangesFilter();
        const tbody = document.getElementById('table-body');
        tbody.classList.remove('fade-in');
        void tbody.offsetWidth;
        tbody.classList.add('fade-in');
    };

    /* --- Escape HTML --- */
    function esc(s) {
        if (s == null) return '';
        return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }

    /* --- Inline word-level diff (like difflib.SequenceMatcher) --- */
    function inlineDiff(oldStr, newStr) {
        const oldWords = String(oldStr ?? '').split(/(\\s+)/);
        const newWords = String(newStr ?? '').split(/(\\s+)/);

        // LCS table for word sequences
        const m = oldWords.length, n = newWords.length;
        const dp = Array.from({length: m + 1}, () => new Uint16Array(n + 1));
        for (let i = 1; i <= m; i++)
            for (let j = 1; j <= n; j++)
                dp[i][j] = oldWords[i-1] === newWords[j-1]
                    ? dp[i-1][j-1] + 1
                    : Math.max(dp[i-1][j], dp[i][j-1]);

        // Backtrack to get opcodes
        const ops = [];
        let i = m, j = n;
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 && oldWords[i-1] === newWords[j-1]) {
                ops.push(['equal', i-1, j-1]);
                i--; j--;
            } else if (j > 0 && (i === 0 || dp[i][j-1] >= dp[i-1][j])) {
                ops.push(['insert', -1, j-1]);
                j--;
            } else {
                ops.push(['delete', i-1, -1]);
                i--;
            }
        }
        ops.reverse();

        let oldHtml = '', newHtml = '';
        for (const [op, oi, ni] of ops) {
            if (op === 'equal') {
                const w = esc(oldWords[oi]);
                oldHtml += w;
                newHtml += w;
            } else if (op === 'delete') {
                oldHtml += '<span class="hi">' + esc(oldWords[oi]) + '</span>';
            } else {
                newHtml += '<span class="hi">' + esc(newWords[ni]) + '</span>';
            }
        }
        return { oldHtml, newHtml };
    }

    /* --- Diff logic --- */
    function renderTable(vIdx) {
        const curr = VERSIONS[vIdx];
        const prev = vIdx > 0 ? VERSIONS[vIdx - 1] : null;
        const cData = curr[DATA_KEY] || [];
        const pData = prev ? (prev[DATA_KEY] || []) : [];

        // Build maps using (key, occurrence) composite keys to handle duplicates
        function buildMap(data) {
            const map = new Map();
            const occ = {};
            for (const r of data) {
                if (r[KEY] == null || r[KEY] === '') continue;
                const k = r[KEY];
                occ[k] = (occ[k] || 0) + 1;
                map.set(k + '\0' + occ[k], r);
            }
            return map;
        }
        const cMap = buildMap(cData);
        const pMap = buildMap(pData);

        // Build ordered list from current version (preserves JSON order, including empty rows)
        const ordered = [];
        const usedKeys = new Set();
        const cOcc = {};
        for (const row of cData) {
            if (row[KEY] == null || row[KEY] === '') {
                ordered.push(null); // spacer
            } else {
                const k = row[KEY];
                cOcc[k] = (cOcc[k] || 0) + 1;
                const ck = k + '\0' + cOcc[k];
                ordered.push(ck);
                usedKeys.add(ck);
            }
        }
        // Append removed rows (in prev but not in curr) at the end
        for (const pk of pMap.keys()) {
            if (!usedKeys.has(pk)) ordered.push(pk);
        }

        let html = '';
        const statusMap = new Map();

        for (let ri = 0; ri < ordered.length; ri++) {
            const k = ordered[ri];
            if (k === null) {
                html += '<tr class="spacer-row"><th></th>'
                    + '<td colspan="' + (COLS.length - 1) + '"></td></tr>';
                continue;
            }

            const c = cMap.get(k);
            const p = pMap.get(k);

            let status = 'unchanged';
            if (!prev) {
                status = 'unchanged';
            } else if (c && !p) {
                status = 'added';
            } else if (!c && p) {
                status = 'removed';
            } else if (c && p) {
                for (const col of COLS) {
                    if (String(c[col] ?? '') !== String(p[col] ?? '')) { status = 'modified'; break; }
                }
            }

            statusMap.set(k, status);

            const item = c || p;
            let cls = '';
            if (status === 'added')    cls = 'diff-added';
            if (status === 'removed')  cls = 'diff-removed';
            if (status === 'modified') cls = 'diff-modified';

            const rowIdx = ri;

            html += '<tr class="' + cls + '">';
            for (let ci = 0; ci < COLS.length; ci++) {
                const col = COLS[ci];
                const cVal = esc(c ? c[col] : item[col]);
                const pVal = esc(p ? p[col] : '');
                let cell;
                if (status === 'modified' && c && p && String(c[col] ?? '') !== String(p[col] ?? '')) {
                    const d = inlineDiff(p[col], c[col]);
                    cell = '<span class="diff-old">' + d.oldHtml + '</span><span class="diff-new">' + d.newHtml + '</span>';
                } else {
                    cell = esc(item[col]);
                }
                const cellClick = status === 'removed'
                    ? ''
                    : ' onclick="showCellDetails(' + rowIdx + ',' + ci + ',this)"';
                if (ci === 0) {
                    html += '<th' + cellClick + '>' + cell + '</th>';
                } else {
                    html += '<td' + cellClick + '>' + cell + '</td>';
                }
            }
            html += '</tr>';
        }

        document.getElementById('table-body').innerHTML = html;

        // Store current diff data for panel use
        window._diffState = { cMap, pMap, ordered, prev, statusMap };
    }

    /* --- Side panel details --- */
    const TAG_LABELS = { added: 'Added', removed: 'Removed', modified: 'Modified' };
    const TAG_CLASSES = { added: 'tag-added', removed: 'tag-removed', modified: 'tag-modified' };

    window.showCellDetails = function(rowIdx, colIdx, cell) {
        const tr = cell.closest('tr');
        setActiveRow(tr);
        const k = window._diffState.ordered[rowIdx];
        const c = window._diffState.cMap.get(k);
        const p = window._diffState.prev ? window._diffState.pMap.get(k) : null;
        const item = c || p;
        const rowStatus = window._diffState.statusMap.get(k) || 'unchanged';
        const col = COLS[colIdx];
        const colLabel = COL_LABELS[colIdx];

        let html = '';

        // Cell full value
        const cVal = c ? String(c[col] ?? '') : '';
        const pVal = p ? String(p[col] ?? '') : '';
        const cellChanged = rowStatus === 'modified' && cVal !== pVal;

        if (cellChanged) {
            const d = inlineDiff(pVal, cVal);
            html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + ' (changed)</div>'
                + '<div class="note-block" style="border-left-color:#d73a49;opacity:0.7;margin-bottom:8px"><span class="diff-old" style="text-decoration:line-through;font-size:inherit;opacity:1">' + d.oldHtml + '</span></div>'
                + '<div class="note-block"><span class="diff-new" style="font-weight:inherit;color:inherit">' + d.newHtml + '</span></div></div>';
        } else {
            const val = String(item[col] ?? '');
            if (val) {
                html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + '</div>'
                    + '<div class="detail-value">' + esc(val) + '</div></div>';
            }
        }

        // Note section
        const note = item[NOTE_FIELD];
        if (note) {
            html += '<div class="detail-section"><div class="detail-label">Note</div>'
                + '<div class="note-block">' + esc(note) + '</div></div>';
        }

        // Panel header: status tag
        const panelTitle = document.getElementById('panel-title');
        if (rowStatus !== 'unchanged') {
            panelTitle.innerHTML = '<span class="status-tag ' + TAG_CLASSES[rowStatus] + '">'
                + TAG_LABELS[rowStatus] + '</span>';
        } else {
            panelTitle.innerHTML = '<span class="status-tag" style="background:#f0f0f5;color:#86868b">No change</span>';
        }
        document.getElementById('panel-body').innerHTML = html;
        openPanel();
    };

    // Initial render
    window.switchVersion(VERSIONS.length - 1);
})();
""")

HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$TITLE</title>
<style>$STYLE</style>
</head>
<body>
<div class="layout">
    <div class="main-content" id="main-content">
        <div class="header-bar">
            <div>
                <h1>$TITLE</h1>
                <p class="subtitle">Click any row for details. Switch versions to track changes.</p>
            </div>
            <div class="controls">
                <div class="control-pill toggle-control">
                    <label for="changes-toggle">Changes only</label>
                    <button class="ios-toggle active" id="changes-toggle" onclick="toggleChangesOnly()" disabled aria-label="Show changes only"></button>
                </div>
                <div class="control-pill version-control">
                    <label for="v-select">Version</label>
                    <select id="v-select" class="version-select" onchange="switchVersion(this.value)"></select>
                </div>
            </div>
        </div>

        <table>
            <thead><tr>$COL_HEADERS</tr></thead>
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

<script>$SCRIPT</script>
</body>
</html>""")
