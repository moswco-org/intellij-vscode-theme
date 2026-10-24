"""Create dark variants of the file icons and make the file icon theme adaptive.

Run after build_file_icons.py:
    python3 scripts/build_file_icons.py . && python3 scripts/build_dark_icons.py .

Writes icons/files-dark/*.svg and rewrites icons/intellij-light-file-icons.json so
the top-level associations use the dark icons and the "light" block uses the
original light icons (VS Code picks the block that matches the active colour theme).
"""
import json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
LIGHT = os.path.join(ROOT, "icons", "files")
DARK = os.path.join(ROOT, "icons", "files-dark")
THEME = os.path.join(ROOT, "icons", "intellij-light-file-icons.json")
os.makedirs(DARK, exist_ok=True)

# New UI Dark icon palette: strokes brighten, tinted fills become deep tints
MAP = {
    "#6C707E": "#CED0D6", "#EBECF0": "#43454A",   # gray
    "#3574F0": "#548AF7", "#E7EFFD": "#25324D",   # blue
    "#208A3C": "#5FB865", "#EEF8F0": "#253627",   # green
    "#E66D17": "#E08855", "#FFF4EB": "#45322B",   # orange
    "#C27D04": "#D6AE58", "#FFF6DE": "#3D3223",   # yellow
    "#8E44C9": "#B189F5", "#F6EDFC": "#2F2936",   # purple
    "#4D5FD6": "#8C9EF5", "#E9ECFB": "#2A2F4A",   # indigo (PHP)
    "#DB3B4B": "#F07A85", "#FFF0F1": "#402929",   # red
    "#1F8A99": "#3DBACC", "#E6F6F8": "#1F3639",   # teal
    "#FFFFFF": "#2B2D30",                         # paper fill
}
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")

count = 0
for f in sorted(os.listdir(LIGHT)):
    if not f.endswith(".svg"):
        continue
    s = open(os.path.join(LIGHT, f)).read()
    def sub(m):
        v = m.group(0).upper()
        if v not in MAP:
            sys.exit(f"{f}: unmapped colour {v}")
        return MAP[v]
    open(os.path.join(DARK, f), "w").write(HEX.sub(sub, s))
    count += 1

t = json.load(open(THEME))
light_defs = {k: v for k, v in t["iconDefinitions"].items() if not k.endswith("_dark")}
assoc_keys = ["file", "folder", "folderExpanded", "rootFolder", "rootFolderExpanded",
              "fileExtensions", "fileNames", "folderNames", "folderNamesExpanded", "languageIds"]
light_block = t.get("light") or {k: t[k] for k in assoc_keys if k in t}

def dark_id(v):
    return v if v.endswith("_dark") else v + "_dark"

defs = dict(light_defs)
for k, v in light_defs.items():
    defs[k + "_dark"] = {"iconPath": v["iconPath"].replace("./files/", "./files-dark/")}

new = {"hidesExplorerArrows": False, "iconDefinitions": defs}
for k in assoc_keys:
    if k not in light_block:
        continue
    v = light_block[k]
    new[k] = {a: dark_id(b) for a, b in v.items()} if isinstance(v, dict) else dark_id(v)
new["light"] = light_block
json.dump(new, open(THEME, "w"), indent=2)
print(count, "dark icons; theme now adaptive (dark default, light override)")
