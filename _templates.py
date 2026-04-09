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

        /* --- Scrollbars: macOS (thin, overlay) --- */
        .os-mac .table-scroll::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        .os-mac .table-scroll::-webkit-scrollbar-track {
            background: transparent;
        }
        .os-mac .table-scroll::-webkit-scrollbar-thumb {
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }
        .os-mac .table-scroll::-webkit-scrollbar-thumb:hover {
            background: rgba(0,0,0,0.35);
            border: 2px solid transparent;
            background-clip: padding-box;
        }
        .os-mac .table-scroll {
            scrollbar-width: thin;
            scrollbar-color: rgba(0,0,0,0.2) transparent;
        }

        /* --- Scrollbars: Windows (always visible) --- */
        .os-win .table-scroll::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        .os-win .table-scroll::-webkit-scrollbar-track {
            background: #f0f0f5;
            border-radius: 5px;
        }
        .os-win .table-scroll::-webkit-scrollbar-thumb {
            background: rgba(0,0,0,0.25);
            border-radius: 5px;
        }
        .os-win .table-scroll::-webkit-scrollbar-thumb:hover {
            background: rgba(0,0,0,0.4);
        }
        .os-win .table-scroll {
            scrollbar-width: auto;
            scrollbar-color: rgba(0,0,0,0.25) #f0f0f5;
        }

        .layout { display: flex; height: 100vh; }

        .main-content {
            flex: 1;
            overflow: hidden;
            padding: 48px 40px;
            display: flex;
            flex-direction: column;
        }

        .table-scroll {
            overflow: auto;
            border-radius: 12px;
            flex: 1;
            min-height: 0;
        }
        .table-scroll.panel-open table {
            margin-right: 420px;
        }

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
            background: #fff;
            border-radius: 12px;
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
            position: sticky;
            top: 0;
            z-index: 3;
        }
        thead th:first-child {
            border-right: 1px solid #d2d2d7;
            position: sticky;
            left: 0;
            z-index: 4;
        }

        tbody th {
            font-size: 13px;
            font-weight: 600;
            color: #49494d;
            background-color: #f9f9fb;
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #f0f0f5;
            border-right: 1px solid #e8e8ed;
            max-width: 180px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            position: sticky;
            left: 0;
            z-index: 2;
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

        tbody tr:nth-child(even):not(.diff-added):not(.diff-removed) th { background-color: #f5f5f7; }
        tbody tr:nth-child(even):not(.diff-added):not(.diff-removed):not(.diff-modified) { background-color: #fafafa; }
        tbody tr:hover:not(.diff-removed):not(.spacer-row) { background-color: #f0f0f5; }

        tbody td.cell-active,
        tbody th.cell-active {
            outline: 2px solid #0071e3;
            outline-offset: -2px;
            border-radius: 2px;
        }

        .diff-added { background-color: #e6ffed !important; }
        .diff-added th { background-color: #e6ffed !important; }
        .diff-added:hover { background-color: #d2fbe0 !important; }
        .diff-added:hover th { background-color: #d2fbe0 !important; }

        .diff-removed { background-color: #ffeef0 !important; color: #a40e26 !important; cursor: not-allowed; }
        .diff-removed td, .diff-removed th { color: #a40e26 !important; text-decoration: line-through; background-color: #ffeef0 !important; }

        td.cell-modified, th.cell-modified { background-color: #fff8c5 !important; }
        td.cell-modified:hover, th.cell-modified:hover { background-color: #fcf1a5 !important; }

        .diff-old { color: #d73a49; margin-right: 6px; font-size: 0.9em; opacity: 0.8; }
        .diff-new { color: #22863a; font-weight: 600; }
        .diff-old .hi { background-color: #fdb8c0; border-radius: 2px; padding: 0 1px; }
        .diff-new .hi { background-color: #acf2bd; border-radius: 2px; padding: 0 1px; }

        .diff-block { display: flex; flex-direction: column; gap: 8px; }
        .diff-line { padding: 6px 8px; border-radius: 4px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }
        .diff-line-old { background-color: #ffeef0; color: #24292e; }
        .diff-line-old .hi { background-color: #fdb8c0; border-radius: 2px; padding: 1px 2px; font-weight: 600; }
        .diff-line-new { background-color: #e6ffed; color: #24292e; }
        .diff-line-new .hi { background-color: #acf2bd; border-radius: 2px; padding: 1px 2px; font-weight: 600; }
        .diff-unified { padding: 6px 8px; border-radius: 4px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; background-color: #f8f8f8; color: #24292e; }
        .diff-unified .hi-del, .diff-unified-inline .hi-del { background-color: #fdb8c0; border-radius: 2px; padding: 1px 2px; color: #a40e26; }
        .diff-unified .hi-add, .diff-unified-inline .hi-add { background-color: #acf2bd; border-radius: 2px; padding: 1px 2px; font-weight: 600; color: #176f2c; }

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
    /* --- OS detection for scrollbar styling --- */
    const isMac = /Mac|iPhone|iPad|iPod/.test(navigator.platform || navigator.userAgent);
    document.body.classList.add(isMac ? 'os-mac' : 'os-win');

    const KEY        = $KEY;
    const DATA_KEY   = $DATA_KEY;
    const COLS       = $COLS;
    const COL_LABELS = $COL_LABELS;
    const NOTE_FIELD = $NOTE_FIELD;
    const VERSIONS   = $VERSIONS;

    let activeCell = null;
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
                    || tr.querySelector('.cell-modified');
                tr.style.display = isDiff ? '' : 'none';
            } else {
                tr.style.display = '';
            }
        });
    }

    /* --- Panel helpers --- */
    const tableScroll = document.querySelector('.table-scroll');
    function openPanel() {
        document.getElementById('detail-panel').classList.add('open');
        tableScroll.classList.add('panel-open');
    }
    function closePanel() {
        document.getElementById('detail-panel').classList.remove('open');
        tableScroll.classList.remove('panel-open');
        if (activeCell) { activeCell.classList.remove('cell-active'); activeCell = null; }
    }
    window.closePanel = closePanel;

    function setActiveCell(cell) {
        if (!cell || cell.closest('tr').classList.contains('diff-removed')) return;
        if (activeCell) activeCell.classList.remove('cell-active');
        cell.classList.add('cell-active');
        activeCell = cell;
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

    /* --- LCS diff on a token array, returns opcodes --- */
    function lcsOps(oldToks, newToks) {
        const m = oldToks.length, n = newToks.length;
        const dp = Array.from({length: m + 1}, () => new Uint16Array(n + 1));
        for (let i = 1; i <= m; i++)
            for (let j = 1; j <= n; j++)
                dp[i][j] = oldToks[i-1] === newToks[j-1]
                    ? dp[i-1][j-1] + 1
                    : Math.max(dp[i-1][j], dp[i][j-1]);
        const ops = [];
        let i = m, j = n;
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 && oldToks[i-1] === newToks[j-1]) {
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
        return ops;
    }

    /* --- Inline diff: character-level for pure add/delete, word-level for mixed --- */
    function inlineDiff(oldStr, newStr) {
        const a = String(oldStr ?? ''), b = String(newStr ?? '');

        // First pass: character-level to detect if add-only or delete-only
        const charOps = lcsOps(a.split(''), b.split(''));
        let charHasInsert = false, charHasDelete = false;
        for (const [op] of charOps) {
            if (op === 'delete') charHasDelete = true;
            if (op === 'insert') charHasInsert = true;
            if (charHasInsert && charHasDelete) break;
        }

        // Add-only or delete-only: use character-level diff with unified view
        if (!(charHasInsert && charHasDelete)) {
            let unifiedHtml = '';
            for (const [op, oi, ni] of charOps) {
                if (op === 'equal') unifiedHtml += esc(a[oi]);
                else if (op === 'delete') unifiedHtml += '<span class="hi-del">' + esc(a[oi]) + '</span>';
                else unifiedHtml += '<span class="hi-add">' + esc(b[ni]) + '</span>';
            }
            return { oldHtml: '', newHtml: '', unifiedHtml, mode: 'unified' };
        }

        // Mixed changes: use word-level diff with split view
        const oldWords = a.split(/(\\s+)/);
        const newWords = b.split(/(\\s+)/);
        const ops = lcsOps(oldWords, newWords);
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
        return { oldHtml, newHtml, unifiedHtml: '', mode: 'split' };
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
            let rowCls = '';
            if (status === 'added')   rowCls = 'diff-added';
            if (status === 'removed') rowCls = 'diff-removed';

            const rowIdx = ri;

            html += '<tr class="' + rowCls + '">';
            for (let ci = 0; ci < COLS.length; ci++) {
                const col = COLS[ci];
                const cVal = esc(c ? c[col] : item[col]);
                const pVal = esc(p ? p[col] : '');
                let cell;
                let cellCls = '';
                if (status === 'modified' && c && p && String(c[col] ?? '') !== String(p[col] ?? '')) {
                    const d = inlineDiff(p[col], c[col]);
                    cell = d.mode === 'unified'
                        ? '<span class="diff-unified-inline">' + d.unifiedHtml + '</span>'
                        : '<span class="diff-old">' + d.oldHtml + '</span><span class="diff-new">' + d.newHtml + '</span>';
                    cellCls = ' cell-modified';
                } else {
                    cell = esc(item[col]);
                }
                const cellClick = status === 'removed'
                    ? ''
                    : ' onclick="showCellDetails(' + rowIdx + ',' + ci + ',this)"';
                const dataAttrs = ' data-row="' + rowIdx + '" data-col="' + ci + '"';
                if (ci === 0) {
                    html += '<th class="' + cellCls + '"' + dataAttrs + cellClick + '>' + cell + '</th>';
                } else {
                    html += '<td class="' + cellCls + '"' + dataAttrs + cellClick + '>' + cell + '</td>';
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
        setActiveCell(cell);
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
            if (d.mode === 'unified') {
                html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + '</div>'
                    + '<div class="detail-value"><div class="diff-unified">' + d.unifiedHtml + '</div></div></div>';
            } else {
                html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + '</div>'
                    + '<div class="detail-value"><div class="diff-block">'
                    + '<div class="diff-line diff-line-old">' + d.oldHtml + '</div>'
                    + '<div class="diff-line diff-line-new">' + d.newHtml + '</div>'
                    + '</div></div></div>';
            }
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

    /* --- Keyboard navigation --- */
    document.addEventListener('keydown', function(e) {
        if (!activeCell) return;
        const arrows = {ArrowUp: [-1,0], ArrowDown: [1,0], ArrowLeft: [0,-1], ArrowRight: [0,1]};
        const dir = arrows[e.key];
        if (!dir) return;
        e.preventDefault();

        const row = parseInt(activeCell.dataset.row);
        const col = parseInt(activeCell.dataset.col);
        const tbody = document.getElementById('table-body');
        const allRows = Array.from(tbody.querySelectorAll('tr'));
        const numCols = COLS.length;

        let newRow = row + dir[0];
        let newCol = col + dir[1];

        // Clamp column
        if (newCol < 0) newCol = 0;
        if (newCol >= numCols) newCol = numCols - 1;

        // Find next valid row (skip spacers and removed rows)
        const maxIdx = allRows.length;
        while (newRow >= 0 && newRow < maxIdx) {
            const tr = allRows[newRow];
            if (!tr.classList.contains('spacer-row') && !tr.classList.contains('diff-removed')) break;
            newRow += dir[0] || 1; // if horizontal move landed on invalid, skip down
        }
        if (newRow < 0 || newRow >= maxIdx) return;

        const target = tbody.querySelector('[data-row="' + newRow + '"][data-col="' + newCol + '"]');
        if (target && target.onclick) {
            target.click();
            target.scrollIntoView({block: 'nearest'});
        }
    });

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

        <div class="table-scroll">
        <table>
            <thead><tr>$COL_HEADERS</tr></thead>
            <tbody id="table-body"></tbody>
        </table>
        </div>
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
