"""HTML, CSS, and JS templates for diffable HTML output."""

from string import Template

TOGGLE_PILL_HTML = """<div class="control-pill toggle-control">
                    <label for="changes-toggle">Changes only</label>
                    <button class="ios-toggle active" id="changes-toggle" onclick="toggleChangesOnly()" disabled aria-label="Show changes only"></button>
                </div>
                """

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
            padding: 40px 40px;
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
            margin-bottom: 24px;
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
            font-size: 13px;
            font-weight: 500;
            color: #86868b;
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
        .status-tag.tag-added    { background: #D9F1D8; color: #1E7E2C; }
        .status-tag.tag-removed  { background: #FFE0DC; color: #C40D1F; }
        .status-tag.tag-modified { background: #FFF5CC; color: #946100; }

        table {
            width: 100%;
            min-width: 600px;
            border-collapse: separate;
            border-spacing: 0;
            background: #fff;
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.08);
        }

        thead th {
            background: #fff;
            font-size: 12px;
            font-weight: 600;
            color: #1d1d1f;
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 3;
        }
        thead th:first-child {
            position: sticky;
            left: 0;
            z-index: 4;
        }

        tbody th {
            font-size: 13px;
            font-weight: 600;
            color: #49494d;
            background-color: #fff;
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(0,0,0,0.06);
            border-right: 1px solid rgba(0,0,0,0.06);
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
            border-bottom: 1px solid rgba(0,0,0,0.06);
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

        /* Subtle zebra striping for long-table scanning. Finder-style:
           white / near-white alternation, just enough to anchor the eye
           across many rows. Added / removed rows opt out so their semantic
           tint isn't overridden. */
        tbody tr:nth-child(even):not(.diff-added):not(.diff-removed) { background-color: #fafafa; }
        tbody tr:nth-child(even):not(.diff-added):not(.diff-removed) th { background-color: #fafafa; }
        tbody tr:hover:not(.diff-removed):not(.spacer-row) { background-color: #f0f0f5; }
        tbody tr:hover:not(.diff-removed):not(.spacer-row) th { background-color: #f0f0f5; }

        tbody td.cell-active,
        tbody th.cell-active {
            outline: 2px solid #0071e3;
            outline-offset: -2px;
            border-radius: 2px;
        }

        .diff-added { background-color: #D9F1D8 !important; }
        .diff-added th { background-color: #D9F1D8 !important; }
        .diff-added:hover { background-color: #BFE5BE !important; }
        .diff-added:hover th { background-color: #BFE5BE !important; }

        /* Removed rows: pink bg only, mirroring how added rows just get a
           green bg. The earlier red strikethrough on every cell was
           visually heavier than any other row type and made the column
           data hard to read. Bg colour alone is enough signal — same
           pattern as GitHub's "removed line" treatment. */
        .diff-removed { background-color: #FFE0DC !important; }
        .diff-removed td, .diff-removed th { background-color: #FFE0DC !important; }


        /* Modified cells stay on the default cell bg — the inline pink/
           green pills on the diff marks are enough signal without a
           cell-level tint adding a third colour to the mix. For value↔
           empty cases the inner span renders as a GitHub-style pill so
           it matches the inline .hi-add / .hi-del rendering elsewhere:
             empty → value (.cell-added-value):   green pill
             value → empty (.cell-removed-value): pink pill */
        .cell-removed-value {
            background-color: #fdb8c0;
            color: #82071e;
            border-radius: 2px;
            padding: 0 2px;
        }
        .cell-added-value {
            background-color: #abf2bc;
            color: #044f1e;
            font-weight: 600;
            border-radius: 2px;
            padding: 0 2px;
        }

        /* --- Inline diff marks ---
           GitHub-style word/character highlights: medium-saturation pink
           pill for deletes with dark red text, medium green pill for
           inserts with dark green semibold text. The light pill bg lets
           the changed run pop within the surrounding cell content
           without dominating it. No strikethrough — the pink colour +
           pill already conveys "removed" on its own. */
        .diff-unified .hi-del, .diff-unified-inline .hi-del,
        .diff-old .hi, .diff-line-old .hi {
            background-color: #fdb8c0;
            color: #82071e;
            border-radius: 2px;
            padding: 0 2px;
        }
        .diff-unified .hi-add, .diff-unified-inline .hi-add,
        .diff-new .hi, .diff-line-new .hi {
            background-color: #abf2bc;
            color: #044f1e;
            font-weight: 600;
            border-radius: 2px;
            padding: 0 2px;
        }

        /* Cell-level split spans (old → new) used for whitespace-text
           mixed changes. Parent styling is restrained; the .hi marks
           inside carry the semantic colour. */
        .diff-old { opacity: 0.7; margin-right: 8px; }
        .diff-new { font-weight: 500; }

        /* Side-panel split blocks. The pink/green row tint frames the
           before/after pair; inner .hi marks (defined above) emphasise
           the specific change without their own fill. */
        .diff-block { display: flex; flex-direction: column; gap: 8px; }
        .diff-line { padding: 8px 12px; border-radius: 6px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }
        .diff-line-old { background-color: #FFF1EE; color: #1d1d1f; }
        .diff-line-new { background-color: #EFF8EF; color: #1d1d1f; }
        /* Placeholder for the empty side of a value↔empty diff block —
           italic dim grey reads as "no content here" instead of as an
           abandoned coloured rectangle. */
        .diff-empty { color: #aeaeb2; font-style: italic; }

        /* Unified-mode block in side panel (fully deleted / added value,
           not split into old/new lines). Single muted background. */
        .diff-unified { padding: 8px 12px; border-radius: 6px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; background-color: #fafafa; color: #1d1d1f; }


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
            font-size: 12px; font-weight: 600;
            color: #86868b; margin-bottom: 6px;
        }
        .detail-value { font-size: 15px; color: #1d1d1f; line-height: 1.5; }

        .note-block {
            background: #f5f5f7;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.6;
            color: #1d1d1f;
            /* Preserve newlines so multi-line notes (e.g. a pin's pull-up
               + pull-down refdes mapping) render as separate lines. */
            white-space: pre-wrap;
        }

        .placeholder {
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            height: calc(100vh - 80px);
            color: #d2d2d7;
        }
        .placeholder-icon { font-size: 48px; margin-bottom: 12px; }
        .placeholder-text { font-size: 15px; color: #86868b; }

        /* --- Time Machine timeline rail ---
           Apple-style two-column rail: month/year labels left of the
           central spine, version names right of the spine. Older at
           top, newer at bottom. Always renders for any non-empty
           timeline (>=1 versions). */
        .timeline-rail {
            /* Two label columns share the rail: months on the left
               (right-aligned), version names on the right (after the
               tick stub). 170px gives both columns enough room. */
            width: 170px;
            flex-shrink: 0;
            align-self: flex-start;
            height: 100vh;
            padding: 48px 0;
            --tl-label-bg: #f5f5f7;
        }

        .timeline-rail-inner {
            position: relative;
            width: 100%;
            height: 100%;
        }

        /* Soft vertical spine in a center column. Month labels sit to
           its left, ticks/version names to its right. */
        .tl-line {
            position: absolute;
            left: 90px;
            top: 0;
            bottom: 0;
            width: 1px;
            background: linear-gradient(180deg,
                transparent 0%,
                #d2d2d7 10%,
                #d2d2d7 90%,
                transparent 100%);
            pointer-events: none;
        }

        .tl-tick {
            position: absolute;
            /* Anchor each tick so its stub starts on the spine and
               extends rightward toward the version label. */
            left: 84px;
            display: flex;
            align-items: center;
            height: 16px;
            transform: translateY(-50%);
            cursor: pointer;
            padding-right: 4px;
            z-index: 2;
            --tl-prox: 0;
        }

        .tl-tick::before {
            content: '';
            display: block;
            width: calc(8px + var(--tl-prox) * 20px);
            height: calc(1px + var(--tl-prox) * 1.5px);
            background: #b8b8c0;
            margin-left: 6px;
            margin-right: 6px;
            flex-shrink: 0;
            transition: background 0.18s ease;
        }

        .tl-tick-label {
            font-family: 'SF Mono', SFMono-Regular, Menlo, monospace;
            /* Default visibility tracks magnifier proximity: non-major
               labels are hidden at rest and fade in as the cursor
               approaches. .tl-tick-major / .tl-tick.active pin opacity
               so first/last/major-bumps and the active version stay
               visible at all times. */
            font-size: calc(10.25px + var(--tl-prox) * 1.5px);
            color: color-mix(in srgb, #86868b, #1d1d1f calc(var(--tl-prox) * 100%));
            opacity: var(--tl-prox);
            transform: translateX(calc(-6px + var(--tl-prox) * 6px));
            white-space: nowrap;
            pointer-events: none;
            background: var(--tl-label-bg);
            padding: 1px 5px;
            border-radius: 3px;
            transition: color 0.18s ease, opacity 0.18s ease;
        }
        .tl-tick-major .tl-tick-label {
            opacity: 1;
            transform: translateX(0);
        }

        .tl-tick:hover::before { background: #1d1d1f; }
        .tl-tick:hover .tl-tick-label { color: #1d1d1f; }

        .tl-tick.active::before {
            width: 24px;
            height: 2px;
            background: #0071e3;
        }
        .tl-tick.active .tl-tick-label {
            opacity: 1;
            transform: translateX(0);
            color: #0071e3;
            font-weight: 600;
        }

        /* Month guideposts — Apple Time Machine convention. Title Case
           ("August"), not all-caps; same size everywhere so the right
           edge stays a clean column. .tl-month-anchor on first row,
           year transitions, and last row bumps weight + colour so the
           year reads as a section break. */
        .tl-month {
            position: absolute;
            /* Right-aligned, ending ~10px before the spine at left:90.
               Rail width 170 → right:90 puts the right edge at x=80. */
            right: 90px;
            transform: translateY(-50%);
            text-align: right;
            font-size: 10px;
            font-weight: 400;
            letter-spacing: 0;
            color: #9a9aa0;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", system-ui, sans-serif;
            pointer-events: none;
            white-space: nowrap;
        }
        .tl-month-anchor {
            font-weight: 600;
            color: #6e6e73;
        }
        /* Clickable month labels jump to the version closest to that
           month on the rail. Override the base pointer-events:none so
           the click lands; hover darkens the ink to match .tl-tick:hover. */
        .tl-month-link {
            cursor: pointer;
            pointer-events: auto;
        }
        .tl-month-link:hover {
            color: #1d1d1f;
        }

        .header-bar.rail-active .version-control { display: none; }

        @media (max-width: 900px) {
            .timeline-rail { display: none; }
            .header-bar.rail-active .version-control { display: flex; }
        }
"""

JS_TEMPLATE = Template("""
(function() {
    /* --- OS detection for scrollbar styling --- */
    const isMac = /Mac|iPhone|iPad|iPod/.test(navigator.platform || navigator.userAgent);
    document.body.classList.add(isMac ? 'os-mac' : 'os-win');

    const KEY          = $KEY;
    const DATA_KEY     = $DATA_KEY;
    const COLS         = $COLS;
    const COL_LABELS   = $COL_LABELS;
    const NOTE_FIELD   = $NOTE_FIELD;
    const VERSIONS     = $VERSIONS;
    const CHANGES_ONLY = $CHANGES_ONLY;

    let activeCell = null;
    let changesOnly = true;

    /* --- Changes-only toggle --- */
    const changesToggle = document.getElementById('changes-toggle');
    window.toggleChangesOnly = function() {
        if (!changesToggle) return;
        changesOnly = !changesOnly;
        changesToggle.classList.toggle('active', changesOnly);
        applyChangesFilter();
    };

    function updateToggleState(vIdx) {
        if (!changesToggle) return;
        const hasPrev = vIdx > 0;
        changesToggle.disabled = !hasPrev;
        if (!hasPrev && changesOnly) {
            changesOnly = false;
            changesToggle.classList.remove('active');
        }
    }

    function applyChangesFilter() {
        // Re-render rather than toggle display: when changesOnly is on we
        // skip unchanged rows entirely in renderTable, so the DOM stays
        // small. Toggling to off rebuilds the full table once.
        const vIdx = parseInt(vSelect.value);
        renderTable(vIdx);
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
        updateVersionTimelineActive(vIdx);
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

        // Fast path: one side is empty. Treat as a dissimilar swap so the
        // cell renderer shows whichever side has data (the gutter accent
        // is the "this cell changed" signal, the side panel carries the
        // full before/after).
        if (a && !b) {
            return { oldHtml: esc(a), newHtml: '',
                     unifiedHtml: '', mode: 'split', dissimilar: true };
        }
        if (!a && b) {
            return { oldHtml: '', newHtml: esc(b),
                     unifiedHtml: '', mode: 'split', dissimilar: true };
        }

        // First pass: character-level diff. Track op presence and the
        // length of the longest common subsequence (count of 'equal' ops),
        // which we'll use as a similarity score below.
        const charOps = lcsOps(a.split(''), b.split(''));
        let charHasInsert = false, charHasDelete = false, equalCount = 0;
        for (const [op] of charOps) {
            if (op === 'delete') charHasDelete = true;
            else if (op === 'insert') charHasInsert = true;
            else equalCount++;
        }

        // Build a unified inline rendering from char-level ops. Equal chars
        // are plain text; deletes get a pink pill, inserts get a green pill.
        // Consecutive same-op chars are merged into one span so a fully
        // deleted/added run renders as one block instead of per-char pills.
        function buildUnifiedHtml() {
            let html = '';
            let buf = '';
            let bufOp = null;
            const flush = () => {
                if (!buf) return;
                if (bufOp === 'equal') html += esc(buf);
                else if (bufOp === 'delete') html += '<span class="hi-del">' + esc(buf) + '</span>';
                else html += '<span class="hi-add">' + esc(buf) + '</span>';
                buf = '';
                bufOp = null;
            };
            for (const [op, oi, ni] of charOps) {
                if (op !== bufOp) flush();
                bufOp = op;
                buf += op === 'insert' ? b[ni] : a[oi];
            }
            flush();
            return html;
        }

        // Build a split (old / new) char-level rendering. Same char-ops,
        // emit each delete on the old side and each insert on the new
        // side, with consecutive same-op chars merged into one .hi span.
        function buildSplitHtml() {
            let oldHtml = '', newHtml = '';
            let oldBuf = '', newBuf = '', op_ = null;
            const flush = () => {
                if (op_ === 'equal') {
                    oldHtml += esc(oldBuf);
                    newHtml += esc(newBuf);
                } else if (op_ === 'delete') {
                    oldHtml += '<span class="hi">' + esc(oldBuf) + '</span>';
                } else if (op_ === 'insert') {
                    newHtml += '<span class="hi">' + esc(newBuf) + '</span>';
                }
                oldBuf = ''; newBuf = ''; op_ = null;
            };
            for (const [op, oi, ni] of charOps) {
                if (op !== op_) flush();
                op_ = op;
                if (op === 'equal') { oldBuf += a[oi]; newBuf += b[ni]; }
                else if (op === 'delete') oldBuf += a[oi];
                else newBuf += b[ni];
            }
            flush();
            return { oldHtml, newHtml };
        }

        // Add-only or delete-only: build BOTH renderings (the cell uses the
        // compact unified one; the side panel can use the before/after
        // split since it has room for two rows and is the easier place
        // to copy from).
        if (!(charHasInsert && charHasDelete)) {
            const mode = charHasDelete ? 'unified-del' : 'unified-add';
            const { oldHtml, newHtml } = buildSplitHtml();
            return { oldHtml, newHtml, unifiedHtml: buildUnifiedHtml(), mode };
        }

        // Similarity gate: when the two strings barely overlap, char- or
        // word-level diff finds spurious matches and renders as a sea of
        // tiny pink/green pills (e.g. CLK_100M_NVME_SSD_1_REFCLKN vs
        // CP10F_CMN0_REFCLK_DN — totally different nets, but they share
        // letters like _, M, R, F, etc.). Below 70% LCS coverage, show
        // the whole old + whole new with no inner highlighting and flag
        // the result as dissimilar so the caller can paint a gutter
        // accent on the cell.
        //
        // Exception: short values (≤ 12 chars, like "10kΩ" → "4.7kΩ")
        // skip the gate. The user can read both old and new at a glance
        // anyway, and the inline rendering ([-10-][+4.7+]kΩ) is more
        // informative than a plain new-value-only fallback.
        const similarity = equalCount / Math.max(a.length, b.length);
        const isShort = Math.max(a.length, b.length) <= 12;
        if (similarity < 0.7 && !isShort) {
            return { oldHtml: esc(a), newHtml: esc(b),
                     unifiedHtml: '', mode: 'split', dissimilar: true };
        }

        // Identifier-like strings (no whitespace, e.g. SCH net names like
        // CP10B_CMN0_REFCLK_DN vs CP10G_CMN0_REFCLK_DN). Build BOTH the
        // unified char-level rendering (used in the compact cell view)
        // and a split before/after rendering (used in the side panel).
        if (!/\\s/.test(a) && !/\\s/.test(b)) {
            const { oldHtml, newHtml } = buildSplitHtml();
            return { oldHtml, newHtml,
                     unifiedHtml: buildUnifiedHtml(), mode: 'unified-mod' };
        }

        // Mixed changes with whitespace (prose): word-level split view.
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

    /* --- Reshape precomputed diff_rows into cData/pData arrays so the
           existing renderer logic below can run unchanged. Only used in
           CHANGES_ONLY mode. --- */
    function reshapeDiffRows(drs) {
        const cData = [], pData = [];
        for (const dr of drs) {
            if (dr.status === 'added') {
                cData.push(dr.curr);
            } else if (dr.status === 'modified') {
                cData.push(dr.curr);
                pData.push(dr.prev);
            } else if (dr.status === 'removed') {
                pData.push(dr.prev);
            }
        }
        return { cData, pData };
    }

    /* --- Diff logic --- */
    function renderTable(vIdx) {
        const curr = VERSIONS[vIdx];
        const prev = vIdx > 0 ? VERSIONS[vIdx - 1] : null;
        let cData, pData;
        if (CHANGES_ONLY) {
            if (vIdx === 0) {
                // Earliest version: nothing to diff against. Render its full
                // baseline data as a plain snapshot (the Python builder
                // keeps the first version's rows under DATA_KEY for this).
                cData = curr[DATA_KEY] || [];
                pData = [];
            } else {
                ({ cData, pData } = reshapeDiffRows(curr.diff_rows || []));
            }
        } else {
            cData = curr[DATA_KEY] || [];
            pData = prev ? (prev[DATA_KEY] || []) : [];
        }

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
                // Compare every key on either side that isn't the note
                // field. Note is auxiliary metadata (shown only in the
                // side panel); a change there alone shouldn't flag the
                // row as modified — matches the Python-side filter in
                // _build_diff_only_versions.
                const allKeys = new Set([...Object.keys(c), ...Object.keys(p)]);
                allKeys.delete(NOTE_FIELD);
                for (const col of allKeys) {
                    if (String(c[col] ?? '') !== String(p[col] ?? '')) { status = 'modified'; break; }
                }
            }

            statusMap.set(k, status);

            // Skip unchanged rows entirely when the filter is on — keeps
            // the DOM small for huge tables (e.g. 3500-pin BGAs). When
            // there's no prior version (vIdx 0 / baseline view) every row
            // is 'unchanged' by default; skipping them would empty the
            // table, so render them as plain data instead.
            if (changesOnly && status === 'unchanged' && prev) continue;

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
                    if (d.dissimilar) {
                        // value↔empty cases get a cell-level tint that
                        // mirrors the row-level .diff-added / .diff-removed.
                        if (cVal === '' && pVal !== '') {
                            cell = '<span class="cell-removed-value">' + pVal + '</span>';
                            cellCls = ' cell-modified cell-removed';
                        } else if (pVal === '' && cVal !== '') {
                            cell = '<span class="cell-added-value">' + cVal + '</span>';
                            cellCls = ' cell-modified cell-added';
                        } else {
                            cell = cVal || pVal;
                            cellCls = ' cell-modified';
                        }
                    } else {
                        cell = d.mode.startsWith('unified')
                            ? '<span class="diff-unified-inline">' + d.unifiedHtml + '</span>'
                            : '<span class="diff-old">' + d.oldHtml + '</span><span class="diff-new">' + d.newHtml + '</span>';
                        cellCls = ' cell-modified';
                    }
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
            // For any unified-* mode where we have both halves of the
            // split rendering, prefer the before/after view in the side
            // panel — the cell stays compact, but the panel has room
            // for two rows which are easier to read and easier to copy.
            if (d.mode.startsWith('unified') && d.oldHtml && d.newHtml) {
                html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + '</div>'
                    + '<div class="detail-value"><div class="diff-block">'
                    + '<div class="diff-line diff-line-old">' + d.oldHtml + '</div>'
                    + '<div class="diff-line diff-line-new">' + d.newHtml + '</div>'
                    + '</div></div></div>';
            } else if (d.mode.startsWith('unified')) {
                html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + '</div>'
                    + '<div class="detail-value"><div class="diff-unified">' + d.unifiedHtml + '</div></div></div>';
            } else {
                // When one side is empty (value↔empty case), drop in an
                // italic-grey "(empty)" placeholder so the diff-line block
                // doesn't render as an orphaned coloured rectangle.
                const oldShown = d.oldHtml || '<span class="diff-empty">(empty)</span>';
                const newShown = d.newHtml || '<span class="diff-empty">(empty)</span>';
                html += '<div class="detail-section"><div class="detail-label">' + esc(colLabel) + '</div>'
                    + '<div class="detail-value"><div class="diff-block">'
                    + '<div class="diff-line diff-line-old">' + oldShown + '</div>'
                    + '<div class="diff-line diff-line-new">' + newShown + '</div>'
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

    /* --- Time Machine timeline rail --- */
    const TL_MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const TL_MONTHS_FULL = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const TL_MONTH_LOOKUP = {
        jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7,
        sep:8, sept:8, oct:9, nov:10, dec:11,
        january:0, february:1, march:2, april:3, june:5, july:6, august:7,
        september:8, october:9, november:10, december:11
    };

    function parseTimelineDate(s) {
        if (!s) return null;
        const str = String(s).trim();
        let m = str.match(/^(\\d{4})-(\\d{1,2})(?:-(\\d{1,2}))?/);
        if (m) {
            const y = parseInt(m[1], 10);
            const mo = parseInt(m[2], 10) - 1;
            const d = m[3] ? parseInt(m[3], 10) : 1;
            return Math.floor(Date.UTC(y, mo, d) / 1000);
        }
        m = str.match(/^([A-Za-z]+)\\s+(\\d{4})$$/);
        if (m) {
            const mi = TL_MONTH_LOOKUP[m[1].toLowerCase()];
            if (mi != null) return Math.floor(Date.UTC(parseInt(m[2], 10), mi, 1) / 1000);
        }
        const t = Date.parse(str);
        if (!isNaN(t)) return Math.floor(t / 1000);
        return null;
    }

    const TL_TEMPORAL_WEIGHT = 0.55;
    // The rail is the only revision selector when the dropdown is
    // hidden (.header-bar.rail-active); render it whenever there's
    // at least one tick. Hide only when there are zero.
    const TL_MIN_TICKS = 1;

    // Identify "major" versions whose labels stay visible at rest.
    //   1. The first version overall is always major.
    //   2. The last version overall is always major.
    //   3. Every version that bumps the major number is major.
    //   4. The very first .X0 version anywhere on the rail is major
    //      (the "first decade" marker — v0.10 in a v0.01-started
    //      timeline). Subsequent .X0s do not requalify.
    // Returns a Set of pre-sort indices that are major.
    function detectMajorIndices(items) {
        const parsed = items
            .map((it, i) => {
                const m = String(it.label || '').match(/v?(\\d+)\\.(\\d+)/);
                return m ? { i: i, ts: it.ts || 0, major: +m[1], minor: +m[2] } : null;
            })
            .filter(Boolean)
            .sort((a, b) => a.ts - b.ts);
        const out = new Set();
        if (!parsed.length) return out;
        const lastIdx = parsed.length - 1;
        let prevMajor = null;
        let firstDecadeSeen = false;
        parsed.forEach((p, idx) => {
            const isFirst    = idx === 0;
            const isLast     = idx === lastIdx;
            const isMajorBmp = !isFirst && p.major !== prevMajor;
            const isFirstDec = !firstDecadeSeen && p.minor !== 0 && p.minor % 10 === 0;
            if (isFirst || isLast || isMajorBmp || isFirstDec) out.add(p.i);
            if (p.minor !== 0 && p.minor % 10 === 0) firstDecadeSeen = true;
            prevMajor = p.major;
        });
        return out;
    }

    function buildVersionTimeline(rail, inner, ticks, onSelect) {
        inner.innerHTML = '';

        if (ticks.length < TL_MIN_TICKS) {
            rail.style.display = 'none';
            return false;
        }
        rail.style.display = '';

        const positive = ticks.filter(t => t.ts && t.ts > 0).map(t => t.ts);
        const anyTs = positive.length > 0;

        const spine = document.createElement('div');
        spine.className = 'tl-line';
        inner.appendChild(spine);

        const tsMin = anyTs ? Math.min.apply(null, positive) : 0;
        const tsMax = anyTs ? Math.max.apply(null, positive) : 1;
        const range = Math.max(1, tsMax - tsMin);
        const n = ticks.length;

        const SECS_PER_MONTH_APPROX = 30.44 * 86400;
        const monthSpan = anyTs ? Math.max(1, Math.round(range / SECS_PER_MONTH_APPROX)) : 1;
        const idealH = 80 + n * 60 + monthSpan * 18;
        rail.style.height = 'min(calc(100vh - 80px), ' + idealH + 'px)';

        // Order by time so uniform-spacing ranks reflect chronology.
        // Without parseable timestamps, keep insertion order.
        const order = anyTs
            ? ticks.map((t, i) => ({ i: i, t: t })).sort((a, b) => (a.t.ts || 0) - (b.t.ts || 0))
            : ticks.map((t, i) => ({ i: i, t: t }));
        const posFromTop = new Array(ticks.length);
        const majorIdx   = detectMajorIndices(ticks.map(t => ({ label: t.label, ts: t.ts })));

        order.forEach((entry, rank) => {
            const t = entry.t;
            let fromTop;
            if (anyTs) {
                const safeTs = t.ts || tsMin;
                // Apple Time Machine convention: oldest at top
                // (fromTop = 0), newest at bottom (fromTop = 1).
                const temporalFromTop = (safeTs - tsMin) / range;
                const uniformFromTop = rank / Math.max(1, n - 1);
                fromTop = TL_TEMPORAL_WEIGHT * temporalFromTop
                        + (1 - TL_TEMPORAL_WEIGHT) * uniformFromTop;
            } else {
                // No timestamps to interpolate against — pure uniform
                // spacing in insertion order. Single-tick rails centre
                // the lone dot so it isn't stranded at an edge.
                fromTop = n > 1 ? rank / (n - 1) : 0.5;
            }
            posFromTop[entry.i] = fromTop;

            const tick = document.createElement('div');
            tick.className = 'tl-tick' + (majorIdx.has(entry.i) ? ' tl-tick-major' : '');
            tick.dataset.idx = t.index;
            tick.style.top = (fromTop * 100).toFixed(3) + '%';
            tick.title = t.title || t.label;
            tick.innerHTML = '<span class="tl-tick-label">' + esc(t.label) + '</span>';
            tick.addEventListener('click', () => onSelect(t.index));
            inner.appendChild(tick);
        });

        // Year / month guideposts need real timestamps to map onto.
        // Skip them on the uniform-spacing fallback (no anyTs).
        if (!anyTs) return true;

        const MIN_LABEL_GAP = 0.04;
        const occupied = [];
        const claim = (pos) => {
            for (const p of occupied) {
                if (p == null) continue;
                if (Math.abs(p - pos) < MIN_LABEL_GAP) return false;
            }
            occupied.push(pos);
            return true;
        };

        // Apple Time Machine label convention: one row per visible
        // month, going chronologically. Year-bearing anchors mark the
        // first label, every year transition, and the last label.
        const SECS_PER_YEAR  = 365.25 * 86400;
        const SECS_PER_MONTH = SECS_PER_YEAR / 12;
        // Render time labels whenever there's any range. The sameBoundary
        // branch below collapses to one label when both ticks share a
        // month — small ranges get a single anchor instead of duplicates.
        if (range > 0) {
            const SNAP_TOLERANCE = 0.05;
            const dMin = new Date(tsMin * 1000);
            const dMax = new Date(tsMax * 1000);
            const firstY = dMin.getUTCFullYear(), firstM = dMin.getUTCMonth();
            const lastY  = dMax.getUTCFullYear(), lastM  = dMax.getUTCMonth();
            const sameBoundary = firstY === lastY && firstM === lastM;
            // Pass 1: collect candidate labels.
            // Pin the first month at fromTop=0 (oldest version's row)
            // and, when distinct, the last month at fromTop=1 (newest
            // version's row) — the natural "monthStart >= tsMin" loop
            // skips months whose 1st falls before tsMin (e.g. tsMin =
            // June 27 → June 1 < tsMin → June dropped without the pin).
            //
            // Each label also carries the closest tick's array index
            // (tickI) so pass 2 can wire a click handler that jumps
            // to that version.
            const firstTickI = order.length ? order[0].i : null;
            const lastTickI  = order.length ? order[order.length - 1].i : null;
            const labels = [{ year: firstY, month: firstM, snap: 0, tickI: firstTickI }];
            claim(0);
            if (!sameBoundary) claim(1);
            // Natural intermediates — strictly between the two pins.
            let curY = firstY;
            let curM = firstM + 1;
            if (curM > 11) { curM = 0; curY++; }
            while (curY < lastY || (curY === lastY && curM < lastM)) {
                const monthStart = Date.UTC(curY, curM, 1) / 1000;
                if (monthStart >= tsMin && monthStart <= tsMax) {
                    const temporalFromTop = (monthStart - tsMin) / range;
                    let snap = temporalFromTop;
                    let bestDist = Infinity;
                    let bestI = null;
                    for (let i = 0; i < posFromTop.length; i++) {
                        const ft = posFromTop[i];
                        if (ft == null) continue;
                        const d = Math.abs(ft - temporalFromTop);
                        if (d < bestDist) { bestDist = d; snap = ft; bestI = i; }
                    }
                    if (bestDist > SNAP_TOLERANCE) snap = temporalFromTop;
                    if (claim(snap)) labels.push({ year: curY, month: curM, snap: snap, tickI: bestI });
                }
                curM++;
                if (curM > 11) { curM = 0; curY++; }
            }
            if (!sameBoundary) labels.push({ year: lastY, month: lastM, snap: 1, tickI: lastTickI });
            // Pass 2: render. First and last are always anchors (year-
            // bearing). Year-transition rows are anchors too.
            let lastYearShown = null;
            labels.forEach((ml, idx) => {
                const isBoundary = idx === 0 || idx === labels.length - 1;
                const showYear   = isBoundary || lastYearShown !== ml.year;
                lastYearShown    = ml.year;
                const clickable  = ml.tickI != null;
                const lbl = document.createElement('div');
                lbl.className = (showYear ? 'tl-month tl-month-anchor' : 'tl-month')
                              + (clickable ? ' tl-month-link' : '');
                lbl.textContent = showYear
                    ? TL_MONTHS_FULL[ml.month] + ' ' + ml.year
                    : TL_MONTHS_FULL[ml.month];
                lbl.style.top = (ml.snap * 100).toFixed(3) + '%';
                if (clickable) {
                    const target = ticks[ml.tickI];
                    lbl.title = 'Jump to ' + (target.label || '');
                    lbl.addEventListener('click', () => onSelect(target.index));
                }
                inner.appendChild(lbl);
            });
        }

        return true;
    }

    function updateVersionTimelineActive(idx) {
        document.querySelectorAll('#timeline-inner .tl-tick').forEach(t => {
            t.classList.toggle('active', parseInt(t.dataset.idx) === idx);
        });
    }

    /* --- Dock-style magnifier --- */
    const TL_MAGNIFIER_RADIUS = 110;
    let _tlMagRafScheduled = false;
    let _tlMagLastY = null;
    function _tlApplyMagnifier() {
        _tlMagRafScheduled = false;
        const rail = document.getElementById('timeline-rail');
        if (!rail) return;
        const ticks = rail.querySelectorAll('.tl-tick');
        if (_tlMagLastY == null) {
            ticks.forEach(t => t.style.setProperty('--tl-prox', '0'));
            return;
        }
        ticks.forEach(t => {
            const r = t.getBoundingClientRect();
            const y = r.top + r.height / 2;
            const d = Math.abs(_tlMagLastY - y);
            const lin = Math.max(0, 1 - d / TL_MAGNIFIER_RADIUS);
            const prox = lin * lin * (3 - 2 * lin);
            t.style.setProperty('--tl-prox', prox.toFixed(3));
        });
    }
    function _tlScheduleMagnifier() {
        if (_tlMagRafScheduled) return;
        _tlMagRafScheduled = true;
        requestAnimationFrame(_tlApplyMagnifier);
    }
    function _tlInstallMagnifier(rail) {
        if (!rail || rail.dataset.tlMagInstalled === '1') return;
        rail.dataset.tlMagInstalled = '1';
        rail.addEventListener('mousemove', (e) => {
            _tlMagLastY = e.clientY;
            _tlScheduleMagnifier();
        });
        rail.addEventListener('mouseleave', () => {
            _tlMagLastY = null;
            _tlScheduleMagnifier();
        });
    }

    /* --- Build the rail before the initial render so the active tick
           lights up in the first paint. --- */
    (function initTimeline() {
        const rail = document.getElementById('timeline-rail');
        const inner = document.getElementById('timeline-inner');
        if (!rail || !inner) return;
        const ticks = VERSIONS.map((v, i) => ({
            index: i,
            label: v.version,
            ts: parseTimelineDate(v.date),
            title: v.version + (v.date ? ' \u00b7 ' + v.date : '')
        }));
        const active = buildVersionTimeline(rail, inner, ticks, (idx) => {
            vSelect.value = idx;
            window.switchVersion(idx);
        });
        if (active) {
            _tlInstallMagnifier(rail);
            const headerBar = document.querySelector('.header-bar');
            if (headerBar) headerBar.classList.add('rail-active');
        }
    })();

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
            </div>
            <div class="controls">
                $TOGGLE_PILL<div class="control-pill version-control">
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

    <aside class="timeline-rail" id="timeline-rail" aria-label="Revision timeline">
        <div class="timeline-rail-inner" id="timeline-inner"></div>
    </aside>

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
