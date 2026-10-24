"""Build an IntelliJ New UI–style product icon font + VS Code product icon theme.

Icons are drawn on a 16×16 grid as strokes, expanded to filled polygons here
(no external tools needed), then packed into a WOFF with fontTools.
"""
import json, math, os, sys
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(os.path.join(OUT, "icons"), exist_ok=True)
W = 1.0  # stroke width in grid units (1px at 16px)
SEG = 28  # circle resolution


# geometry helpers ------------------------------------------------------------
def area(c):
    return sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c))) / 2


def orient(c, cw=True):
    # y-down grid: positive shoelace area == clockwise on screen
    return c if (area(c) > 0) == cw else c[::-1]


def circle(cx, cy, r, n=SEG):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


class Icon:
    def __init__(self):
        self.contours = []  # (points, is_hole)

    def disc(self, cx, cy, r):
        self.contours.append((circle(cx, cy, r), False)); return self

    def ring(self, cx, cy, r, w=W):
        self.contours.append((circle(cx, cy, r + w / 2), False))
        self.contours.append((circle(cx, cy, r - w / 2), True)); return self

    def poly(self, pts):
        self.contours.append((list(pts), False)); return self

    def seg(self, a, b, w=W, cap=True):
        (x1, y1), (x2, y2) = a, b
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1e-6
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        self.contours.append(([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], False))
        if cap:
            self.contours.append((circle(x1, y1, w / 2, 12), False))
            self.contours.append((circle(x2, y2, w / 2, 12), False))
        return self

    def line(self, *pts, closed=False, w=W):
        pts = list(pts)
        if closed:
            pts.append(pts[0])
        for a, b in zip(pts, pts[1:]):
            self.seg(a, b, w)
        return self

    def arc(self, cx, cy, r, a0, a1, w=W, n=None):
        n = n or max(4, int(abs(a1 - a0) / 12))
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        return self.line(*pts, w=w)

    def rrect(self, x, y, w, h, r=1.5, sw=W):
        """Stroked rounded rectangle; x/y/w/h describe the stroke centerline."""
        self.arc(x + r, y + r, r, 180, 270, sw, 4); self.arc(x + w - r, y + r, r, 270, 360, sw, 4)
        self.arc(x + w - r, y + h - r, r, 0, 90, sw, 4); self.arc(x + r, y + h - r, r, 90, 180, sw, 4)
        self.seg((x + r, y), (x + w - r, y), sw); self.seg((x + w, y + r), (x + w, y + h - r), sw)
        self.seg((x + w - r, y + h), (x + r, y + h), sw); self.seg((x, y + h - r), (x, y + r), sw)
        return self

    def frect(self, x, y, w, h, r=1.0):
        pts = []
        for cx, cy, a in [(x + w - r, y + r, 270), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]:
            pts += [(cx + r * math.cos(math.radians(a + 90 * i / 6)), cy + r * math.sin(math.radians(a + 90 * i / 6))) for i in range(7)]
        return self.poly(pts)


# icon drawings ---------------------------------------------------------------
def folder(i=None):
    i = i or Icon()
    return i.line((2, 3), (6, 3), (7.5, 4.5), (14, 4.5), (14, 13), (2, 13), closed=True)


def doc(i=None):
    i = i or Icon()
    return i.line((3.5, 1.5), (9.5, 1.5), (12.5, 4.5), (12.5, 14.5), (3.5, 14.5), closed=True).line((9.5, 1.5), (9.5, 4.5), (12.5, 4.5))


def plus(i, cx, cy, r):
    return i.seg((cx - r, cy), (cx + r, cy)).seg((cx, cy - r), (cx, cy + r))


def gear():
    i, pts, teeth = Icon(), [], 8
    for k in range(teeth):
        base = 360 / teeth * k
        for da, r in [(-13, 6.6), (13, 6.6), (22.5 - 9, 4.9), (22.5 + 9, 4.9)]:
            a = math.radians(base + da)
            pts.append((8 + r * math.cos(a), 8 + r * math.sin(a)))
    return i.line(*pts, closed=True).ring(8, 8, 2.1)


def bug():
    i = Icon().rrect(5, 5, 6, 9, 3).seg((5, 9.5), (11, 9.5)).seg((8, 9.5), (8, 14))
    i.arc(8, 5, 2, 180, 360, n=8)
    for y, dx in [(7, 0), (10, 0), (13, 0)]:
        i.seg((5, y), (2.5, y - 1 if y == 7 else (y + 1 if y == 13 else y)))
        i.seg((11, y), (13.5, y - 1 if y == 7 else (y + 1 if y == 13 else y)))
    return i


def bell(dot=False):
    i = Icon().line((2.5, 12), (3.8, 10.5), (3.8, 7)).arc(8, 7, 4.2, 180, 360).line((12.2, 7), (12.2, 10.5), (13.5, 12))
    i.seg((2.5, 12), (13.5, 12)).arc(8, 12.6, 1.7, 0, 180, n=6)
    if dot:
        i.disc(12.5, 3.5, 2.2)
    return i


def chevron(d):
    pts = {"r": [(6, 3.5), (10.5, 8), (6, 12.5)], "l": [(10, 3.5), (5.5, 8), (10, 12.5)],
           "d": [(3.5, 6), (8, 10.5), (12.5, 6)], "u": [(3.5, 10), (8, 5.5), (12.5, 10)]}[d]
    return Icon().line(*pts)


def refresh():
    i = Icon().arc(8, 8, 5.5, -60, 230)
    return i.line((10.4, 0.9), (10.75, 3.24), (13.2, 3.5))


def play():
    return Icon().poly([(4.5, 2.6), (13.4, 8), (4.5, 13.4)]).line((4.5, 2.6), (13.4, 8), (4.5, 13.4), closed=True)


def warning():
    return Icon().line((8, 1.8), (14.6, 13.8), (1.4, 13.8), closed=True).seg((8, 6), (8, 9.5)).disc(8, 11.7, .75)


def branch():
    i = Icon().ring(4.5, 3.5, 1.6).ring(4.5, 12.5, 1.6).ring(11.5, 4.5, 1.6).seg((4.5, 5.1), (4.5, 10.9))
    pts = [(11.5 - 7 * t ** 1.5 * 0 - 0, 0) for t in []]
    # S-curve from branch head to trunk
    curve = [(11.5 + (4.5 - 11.5) * t, 6.1 + (10.9 - 6.1) * (3 * t * t - 2 * t ** 3)) for t in [k / 10 for k in range(11)]]
    curve = [(x, y) for x, y in [(11.5, 6.1), (11.5, 7.6), (10.6, 8.6), (8, 9.1), (5.6, 9.6), (4.5, 10.6)]]
    return i.line(*curve)


def database():
    i = Icon()
    # top ellipse ring (approx with polyline)
    pts = [(8 + 5.5 * math.cos(math.radians(a)), 3.8 + 2 * math.sin(math.radians(a))) for a in range(0, 360, 15)]
    i.line(*pts, closed=True)
    i.seg((2.5, 3.8), (2.5, 12.2)).seg((13.5, 3.8), (13.5, 12.2))
    for cy in (8, 12.2):
        i.line(*[(8 + 5.5 * math.cos(math.radians(a)), cy + 2 * math.sin(math.radians(a))) for a in range(0, 181, 15)])
    return i


def lightbulb():
    i = Icon().arc(8, 6.5, 4.5, 140, 400)
    i.line((4.6, 9.4), (5.8, 11.2), (10.2, 11.2), (11.4, 9.4))
    return i.seg((6, 13.5), (10, 13.5))


def flask():
    return Icon().line((6, 1.5), (6, 6), (2.5, 13), (3.3, 14.5), (12.7, 14.5), (13.5, 13), (10, 6), (10, 1.5)).seg((5, 1.5), (11, 1.5)).seg((4.3, 10), (11.7, 10))


ICONS = {
    # activity bar (matches the PhpStorm tool-window strip in the screenshot)
    "folder": folder(),
    "search": Icon().ring(7, 7, 4.6).seg((10.4, 10.4), (14.2, 14.2)),
    "commit": Icon().ring(8, 8, 2.6).seg((8, 1.5), (8, 5.4)).seg((8, 10.6), (8, 14.5)),
    "bug": bug(),
    "plugins": Icon().rrect(2, 2, 5, 5, 1.2).rrect(2, 9, 5, 5, 1.2).rrect(9, 9, 5, 5, 1.2).line((11.5, 1.6), (14.4, 4.5), (11.5, 7.4), (8.6, 4.5), closed=True),
    "account": Icon().ring(8, 5.5, 2.8).arc(8, 15, 5.5, 200, 340),
    "gear": gear(),
    "bell": bell(),
    "bell-dot": bell(True),
    "terminal": Icon().rrect(1.5, 2.5, 13, 11, 1.5).line((4.5, 6), (6.5, 8), (4.5, 10)).seg((8, 10.5), (11.5, 10.5)),
    "database": database(),
    "flask": flask(),
    "structure": Icon().rrect(1.5, 1.5, 5, 4, 1).rrect(9.5, 6, 5, 4, 1).rrect(9.5, 11, 5, 4, 1).line((4, 5.5), (4, 13), (9.5, 13)).seg((4, 8), (9.5, 8)),
    # navigation / tree
    "chevron-right": chevron("r"), "chevron-left": chevron("l"), "chevron-down": chevron("d"), "chevron-up": chevron("u"),
    "close": Icon().seg((4, 4), (12, 12)).seg((12, 4), (4, 12)),
    "add": plus(Icon(), 8, 8, 5.5),
    "ellipsis": Icon().disc(3, 8, 1.2).disc(8, 8, 1.2).disc(13, 8, 1.2),
    "kebab": Icon().disc(8, 3, 1.2).disc(8, 8, 1.2).disc(8, 13, 1.2),
    "collapse": Icon().line((4, 3), (8, 6.5), (12, 3)).line((4, 13), (8, 9.5), (12, 13)),
    "new-file": plus(doc(), 8, 9.5, 2.3),
    "new-folder": plus(folder(), 8, 9, 2.3),
    "filter": Icon().line((2, 2.5), (14, 2.5), (9.5, 8.5), (9.5, 13.5), (6.5, 12), (6.5, 8.5), closed=True),
    "split": Icon().rrect(1.5, 2.5, 13, 11, 1.5).seg((8, 2.5), (8, 13.5)),
    "refresh": refresh(),
    "file": doc(),
    # run / debug (green run arrow, red stop square in the toolbar)
    "play": play(),
    "stop": Icon().frect(3.5, 3.5, 9, 9, 1.4),
    "dot": Icon().disc(8, 8, 3.5),
    "breakpoint": Icon().disc(8, 8, 4.8),
    "breakpoint-ring": Icon().ring(8, 8, 4.3),
    "check": Icon().line((3, 8.5), (6.5, 12), (13, 4.5)),
    "error": Icon().ring(8, 8, 6.2).seg((5.7, 5.7), (10.3, 10.3)).seg((10.3, 5.7), (5.7, 10.3)),
    "warning": warning(),
    "info": Icon().ring(8, 8, 6.2).seg((8, 7.3), (8, 11.5)).disc(8, 4.9, .8),
    "lightbulb": lightbulb(),
    "branch": branch(),
    # window chrome
    "chrome-close": Icon().seg((3.5, 3.5), (12.5, 12.5), cap=False).seg((12.5, 3.5), (3.5, 12.5), cap=False),
    "chrome-minimize": Icon().seg((3, 8), (13, 8), cap=False),
    "chrome-maximize": Icon().rrect(3, 3, 10, 10, .6),
    "chrome-restore": Icon().rrect(3, 5, 8, 8, .6).line((5, 3), (13, 3), (13, 11)),
}

# codicon id -> glyph
MAP = {
    "files": "folder", "explorer-view-icon": "folder",
    "search": "search", "search-view-icon": "search",
    "source-control": "commit", "source-control-view-icon": "commit", "git-commit": "commit",
    "debug-alt": "bug", "debug-alt-small": "bug", "run-view-icon": "bug", "debug": "bug",
    "extensions": "plugins", "extensions-view-icon": "plugins",
    "account": "account", "accounts-view-bar-icon": "account",
    "settings-gear": "gear", "settings-view-bar-icon": "gear", "gear": "gear", "settings": "gear",
    "bell": "bell", "bell-dot": "bell-dot", "notifications-view-icon": "bell",
    "terminal": "terminal", "terminal-view-icon": "terminal",
    "database": "database", "beaker": "flask", "testing-view-icon": "flask",
    "symbol-structure": "structure", "outline-view-icon": "structure", "list-tree": "structure",
    "chevron-right": "chevron-right", "chevron-left": "chevron-left", "chevron-down": "chevron-down", "chevron-up": "chevron-up",
    "tree-item-expanded": "chevron-down", "explorer-view-twistie": "chevron-down",
    "close": "close", "remove-close": "close", "notifications-clear": "close",
    "add": "add", "plus": "add",
    "ellipsis": "ellipsis", "more": "ellipsis", "toolbar-more": "ellipsis", "kebab-vertical": "kebab",
    "collapse-all": "collapse", "new-file": "new-file", "new-folder": "new-folder", "filter": "filter",
    "split-horizontal": "split", "refresh": "refresh", "debug-restart": "refresh", "debug-rerun": "refresh", "sync": "refresh",
    "file": "file", "go-to-file": "file",
    "play": "play", "run": "play", "debug-start": "play", "debug-continue": "play", "run-all": "play", "testing-run-icon": "play",
    "debug-stop": "stop", "primitive-square": "stop", "stop-circle": "stop", "debug-disconnect": "stop",
    "circle-filled": "dot", "close-dirty": "dot", "primitive-dot": "dot",
    "debug-breakpoint": "breakpoint", "debug-breakpoint-unverified": "breakpoint-ring", "debug-breakpoint-disabled": "breakpoint-ring",
    "check": "check", "pass": "check", "testing-passed-icon": "check",
    "error": "error", "warning": "warning", "info": "info",
    "lightbulb": "lightbulb", "lightbulb-autofix": "lightbulb",
    "git-branch": "branch", "source-control-sync": "refresh",
    "chrome-close": "chrome-close", "chrome-minimize": "chrome-minimize", "chrome-maximize": "chrome-maximize", "chrome-restore": "chrome-restore",
}

# font build ------------------------------------------------------------------
UPM, S = 1000, 1000 / 16
names = list(ICONS)
cmap = {0xE001 + k: n for k, n in enumerate(names)}
glyphs = {".notdef": TTGlyphPen(None).glyph()}
for n, icon in ICONS.items():
    pen = TTGlyphPen(None)
    for pts, hole in icon.contours:
        pts = orient(pts, cw=not hole)  # screen-CW outer -> font CW (y flip) handled below
        fpts = [(round(x * S), round((16 - y) * S)) for x, y in pts]
        # after y-flip orientation reverses; TrueType wants outer contours clockwise in y-up space
        fpts = fpts[::-1]
        pen.moveTo(fpts[0])
        for p in fpts[1:]:
            pen.lineTo(p)
        pen.closePath()
    g = pen.glyph()
    if g.numberOfContours > 0:
        g.flags[0] |= 0x40  # OVERLAP_SIMPLE so CoreText unions overlaps
    glyphs[n] = g

fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder([".notdef"] + names)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics({n: (UPM, 0) for n in [".notdef"] + names})
fb.setupHorizontalHeader(ascent=1000, descent=0)
fb.setupNameTable({"familyName": "IntelliJ Light Product Icons", "styleName": "Regular"})
fb.setupOS2(sTypoAscender=1000, sTypoDescender=0, usWinAscent=1000, usWinDescent=0)
fb.setupPost()
fb.font.flavor = "woff"
fb.save(os.path.join(OUT, "icons", "intellij-product-icons.woff"))

code = {n: c for c, n in cmap.items()}
theme = {
    "fonts": [{"id": "intellij-product-icons",
               "src": [{"path": "./intellij-product-icons.woff", "format": "woff"}],
               "weight": "normal", "style": "normal"}],
    "iconDefinitions": {k: {"fontCharacter": "\\" + format(code[v], "X")} for k, v in sorted(MAP.items())},
}
with open(os.path.join(OUT, "icons", "intellij-product-icons.json"), "w") as f:
    json.dump(theme, f, indent=2)
json.dump({n: format(c, "X") for n, c in code.items()}, open("glyphmap.json", "w"))
print(len(names), "glyphs,", len(MAP), "codicon overrides")
