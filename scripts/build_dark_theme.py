"""Derive the IntelliJ Dark IDE colour theme from the light theme.

Keeps the light file's sections and comments, swapping every colour through
role-aware maps (New UI Dark palette). Fails loudly on any unmapped colour so
the two variants never drift apart.

usage: python3 scripts/build_dark_theme.py <extension-root>
"""
import re, sys, os

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SRC = os.path.join(ROOT, "themes", "intellij-light-ide-color-theme.json")
DST = os.path.join(ROOT, "themes", "intellij-dark-ide-color-theme.json")

# ── UI colours (the "colors" block), light → dark ─────────────────────────────
UI = {
    "#1d1f23": "#dfe1e5",  # primary text
    "#3574f0": "#3574f0",  # accent
    "#ffffff": "#1e1f22",  # editor / content surface
    "#e53935": "#db5c5c",  # error
    "#6c707e": "#868a91",  # secondary text
    "#f6f8fa": "#2b2d30",  # tool-window chrome
    "#dfe1e5": "#393b40",  # border
    "#a4a8b2": "#5a5d63",  # muted
    "#ebecf0": "#393b40",
    "#871094": "#c77dbb",
    "#e8a33d": "#f2c55c",  # warning
    "#c9ccd6": "#4e5157",
    "#00000000": "#00000000",
    "#208a3c": "#5fb865",  # success / run
    "#0033b3": "#cf8e6d",
    "#dfe3ea": "#393b40",  # hover / pressed chrome
    "#474a54": "#9da0a8",
    "#f2f6fe": "#26282e",  # current line
    "#eaeef2": "#27292d",  # status bar / panel header
    "#e67e22": "#e08855",
    "#dfe9fc": "#2e436e",
    "#dddddd": "#43454a",  # popup border
    "#d5e1ff": "#2e436e",  # popup selection
    "#8c8c8c": "#7a7e85",
    "#ffd34d": "#32593d",  # find match
    "#f2f4f5": "#2b2d30",  # tab strip
    "#d3d5db": "#4e5157",
    "#067d17": "#6aab73",
    "#d3d8e0": "#43454a",
    "#a6d2ff": "#214283",  # selection
    "#9e880d": "#b3ae60",
    "#8e44c9": "#b189f5",
    "#3574f01a": "#3574f026",
    "#2862d8": "#366ace",
    "#fff6de": "#3d3223",
    "#ffeb9c": "#32593d",
    "#fbfcfd": "#1a1b1e",
    "#e8edf5": "#373b45",
    "#b4dcbd": "#4f7a52",
    "#a8c2f7": "#3f5f9e",
    "#8c8c8c33": "#8c8c8c33",
    "#3574f040": "#3574f059",
    "#1750eb": "#2aacb8",
    "#0000001a": "#00000066",
    "#ffffff66": "#ffffff66",
    "#fff0f1": "#402929",
    "#ffeb9c99": "#32593d99",
    "#ffeb9c80": "#32593d80",
    "#f6e3fa": "#44344a",
    "#f0f2f5": "#2b2d30",
    "#eef1f4": "#27292d",  # title bar
    "#eceef2": "#303236",
    "#ebedf0": "#303236",
    "#e7effd": "#25324d",
    "#e57373": "#b85c5c",
    "#e5393526": "#db5c5c33",
    "#e5393512": "#db5c5c1a",
    "#e4e6eb": "#393b40",
    "#c75450": "#d1675a",
    "#c27d04": "#f2c55c",
    "#b0b4bd": "#5a5d63",
    "#a6d2ff80": "#21428380",
    "#8c8c8c80": "#8c8c8c80",
    "#8c8c8c59": "#8c8c8c59",
    "#8c8c8c4d": "#8c8c8c4d",
    "#8c8c8c1a": "#8c8c8c1a",
    "#3574f014": "#3574f01f",
    "#208a3c40": "#5fb86540",
    "#208a3c26": "#5fb86533",
    "#208a3c14": "#5fb8651a",
    "#208a3c12": "#5fb8651a",
    "#00000080": "#00000080",
    "#0000000f": "#00000040",
}

# Per-key overrides where a role differs from the value map above
UI_KEY = {
    # popups & floating surfaces sit on the chrome colour in New UI Dark
    **{k: "#2b2d30" for k in [
        "editorWidget.background", "editorHoverWidget.background", "editorSuggestWidget.background",
        "editorActionList.background", "menu.background", "quickInput.background", "notifications.background",
        "dropdown.background", "dropdown.listBackground", "debugToolBar.background", "breadcrumbPicker.background",
        "listFilterWidget.background", "editorMarkerNavigation.background", "commandCenter.background",
        "welcomePage.tileBackground", "button.secondaryBackground", "editorStickyScroll.background",
    ]},
    # foregrounds that stay white on coloured fills
    **{k: "#ffffff" for k in [
        "button.foreground", "badge.foreground", "activityBarBadge.foreground", "radio.activeForeground",
        "statusBarItem.errorForeground", "statusBarItem.warningForeground", "scmGraph.historyItemHoverLabelForeground",
        "terminal.ansiBrightWhite",
    ]},
    # selected tree row: white-on-grey in light → blue row in dark
    "list.activeSelectionBackground": "#2e436e",
    "list.focusBackground": "#2e436e",
    "list.inactiveSelectionBackground": "#393b40",
    "activityBar.activeBackground": "#3d3f43",
    "icon.foreground": "#ced0d6",
    "activityBar.foreground": "#ced0d6",
    "activityBar.inactiveForeground": "#9da0a8",
    "editorLineNumber.foreground": "#4b5059",
    "editorLineNumber.activeForeground": "#a1a3ab",
    "editor.foreground": "#bcbec4",
    "terminal.foreground": "#bcbec4",
    "editorCursor.foreground": "#ced0d6",
    "terminalCursor.foreground": "#ced0d6",
    "textLink.foreground": "#548af7",
    "textLink.activeForeground": "#6c9cf8",
    "notificationLink.foreground": "#548af7",
    "editorLink.activeForeground": "#548af7",
    "list.highlightForeground": "#548af7",
    "list.focusHighlightForeground": "#548af7",
    "editorSuggestWidget.highlightForeground": "#548af7",
    "editorSuggestWidget.focusHighlightForeground": "#6c9cf8",
    "editorHoverWidget.highlightForeground": "#548af7",
    "gitDecoration.modifiedResourceForeground": "#6c9cf8",
    "gitDecoration.renamedResourceForeground": "#6c9cf8",
    "gitDecoration.stageModifiedResourceForeground": "#6c9cf8",
    "settings.modifiedItemIndicator": "#548af7",
    "editorBracketHighlight.foreground1": "#bcbec4",
    "editorBracketHighlight.foreground2": "#bcbec4",
    "editorBracketHighlight.foreground3": "#bcbec4",
    "editorBracketMatch.background": "#43454a",
    "editorOverviewRuler.findMatchForeground": "#a68a2b",
    "minimap.findMatchHighlight": "#a68a2b",
    "editor.findMatchBackground": "#32593d",
    "editor.findMatchHighlightBackground": "#32593d99",
    "editorActionList.foreground": "#c77dbb",
    "editorGutter.background": "#1e1f22",
    "minimap.background": "#1e1f22",
    "input.background": "#1e1f22",
    "checkbox.background": "#1e1f22",
    "tab.activeBackground": "#1e1f22",
    "tab.unfocusedActiveBackground": "#1e1f22",
    "editorGroupHeader.noTabsBackground": "#1e1f22",
    "peekViewResult.background": "#2b2d30",
    "widget.border": "#43454a",
    "window.activeBorder": "#1e1f22",
    "window.inactiveBorder": "#1e1f22",
    "sideBar.border": "#1e1f22",
    "activityBar.border": "#1e1f22",
    "panel.border": "#1e1f22",
    "statusBar.border": "#1e1f22",
    "titleBar.border": "#1e1f22",
    "editorGroupHeader.tabsBorder": "#1e1f22",
    "editorGroupHeader.border": "#1e1f22",
    "tab.border": "#1e1f22",
    "textCodeBlock.background": "#2b2d30",
    "textPreformat.foreground": "#bcbec4",
    # Darcula console colours
    "terminal.ansiBlack": "#1e1f22", "terminal.ansiRed": "#f0524f", "terminal.ansiGreen": "#5c962c",
    "terminal.ansiYellow": "#a68a0d", "terminal.ansiBlue": "#3993d4", "terminal.ansiMagenta": "#a771bf",
    "terminal.ansiCyan": "#00a3a3", "terminal.ansiWhite": "#808080", "terminal.ansiBrightBlack": "#595959",
    "terminal.ansiBrightRed": "#ff4050", "terminal.ansiBrightGreen": "#4fc414", "terminal.ansiBrightYellow": "#e5bf00",
    "terminal.ansiBrightBlue": "#1fb0ff", "terminal.ansiBrightMagenta": "#ed7eed", "terminal.ansiBrightCyan": "#00e5e5",
}

# ── Syntax colours (semanticTokenColors + tokenColors) ─────────────────────────
SYN = {
    "#1d1f23": "#bcbec4",  # default text, classes, namespaces
    "#0033b3": "#cf8e6d",  # keywords
    "#067d17": "#6aab73",  # strings
    "#8c8c8c": "#7a7e85",  # comments
    "#871094": "#c77dbb",  # variables / properties / constants
    "#00627a": "#56a8f5",  # functions & methods
    "#1750eb": "#2aacb8",  # numbers
    "#0037a6": "#cf8e6d",  # escapes
    "#9e880d": "#b3ae60",  # attributes / decorators
    "#174ad4": "#bababa",  # HTML attribute names
    "#3574f0": "#548af7",  # links, markup.changed
    "#e53935": "#f75464",
    "#bc3f3c": "#f75464",
    "#20999d": "#16baac",  # type parameters
}
SYN_RULE = {  # by tokenColors "name"
    "Doc comment": "#5f826b",
    "Doc tag (@param, @throws…)": "#67a37c",
    "Tag": "#d5b778",
}

HEADER = """// IntelliJ Dark IDE — colour theme for VS Code (PhpStorm New UI Dark)
// GENERATED from intellij-light-ide-color-theme.json by scripts/build_dark_theme.py —
// edit the light theme or the maps in that script, then regenerate.
// Palette
//   text #dfe1e5 / code #bcbec4 · secondary #868a91 · muted #5a5d63 · border #393b40
//   chrome #2b2d30 · editor #1e1f22 · accent #3574f0 · link #548af7
//   green #5fb865 · red #db5c5c · yellow #f2c55c
"""

HEX = re.compile(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?\b")
KEY = re.compile(r'^\s*"([\w.\-]+)"\s*:\s*"#')
NAME = re.compile(r'"name"\s*:\s*"([^"]+)"')

src = open(SRC, encoding="utf-8").read().split("\n")
# drop the light header comment block (everything before the first "{")
start = next(i for i, l in enumerate(src) if l.strip() == "{")
out, section, rule, missing = [], "colors", None, set()

for line in src[start:]:
    if '"semanticTokenColors"' in line:
        section = "syntax"
    m = NAME.search(line)
    if section == "syntax" and m:
        rule = m.group(1)
    if section == "syntax" and (line.strip() == "{" or (line.strip().startswith("{") and '"scope"' in line)):
        rule = None  # inline unnamed rule
    if '"name": "IntelliJ Light IDE"' in line:
        line = line.replace("IntelliJ Light IDE", "IntelliJ Dark IDE")
    if '"type": "light"' in line:
        line = line.replace('"light"', '"dark"')

    def sub(mt):
        v = mt.group(0).lower()
        if section == "colors":
            k = KEY.match(line)
            if k and k.group(1) in UI_KEY:
                return UI_KEY[k.group(1)]
            if v not in UI:
                missing.add(("ui", v)); return v
            return UI[v]
        if rule in SYN_RULE:
            return SYN_RULE[rule]
        if v not in SYN:
            missing.add(("syn", v)); return v
        return SYN[v]

    if not line.lstrip().startswith("//"):
        line = HEX.sub(sub, line)
    out.append(line)

if missing:
    sys.exit(f"unmapped colours: {sorted(missing)}")
open(DST, "w", encoding="utf-8").write(HEADER + "\n".join(out))
print("wrote", DST)
