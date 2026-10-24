"""Generate the IntelliJ New UI–style file icon theme (SVGs + icon theme JSON)."""
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
ICON_DIR = os.path.join(OUT, "icons", "files")
os.makedirs(ICON_DIR, exist_ok=True)

# New UI palette ------------------------------------------------------------
GRAY, GRAY_BG = "#6C707E", "#EBECF0"
BLUE, BLUE_BG = "#3574F0", "#E7EFFD"
GREEN, GREEN_BG = "#208A3C", "#EEF8F0"
ORANGE, ORANGE_BG = "#E66D17", "#FFF4EB"
YELLOW, YELLOW_BG = "#C27D04", "#FFF6DE"
PURPLE, PURPLE_BG = "#8E44C9", "#F6EDFC"
INDIGO, INDIGO_BG = "#4D5FD6", "#E9ECFB"
RED, RED_BG = "#DB3B4B", "#FFF0F1"
TEAL, TEAL_BG = "#1F8A99", "#E6F6F8"

FONT = "'JetBrains Mono','Inter',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">{body}</svg>\n'


def write(name, body):
    with open(os.path.join(ICON_DIR, name + ".svg"), "w") as f:
        f.write(svg(body))


# Shapes ----------------------------------------------------------------------
FOLDER = "M1.5 3.5a1 1 0 0 1 1-1h3.59a1 1 0 0 1 .7.29L8.21 4.2a1 1 0 0 0 .7.3H13.5a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1z"
FOLDER_OPEN_BACK = "M1.5 12V3.5a1 1 0 0 1 1-1h3.59a1 1 0 0 1 .7.29L8.21 4.2a1 1 0 0 0 .7.3H12.5a1 1 0 0 1 1 1V7"
FOLDER_OPEN_FRONT = "M1.5 12.5 3.77 7.5a1 1 0 0 1 .92-.5h9.7a.5.5 0 0 1 .46.7l-2.08 4.5a.5.5 0 0 1-.46.3z"
DOC = "M3.5 2.5a1 1 0 0 1 1-1h5l3 3v9a1 1 0 0 1-1 1h-7a1 1 0 0 1-1-1z"
DOC_FOLD = "M9.5 1.5v3h3"


def folder(stroke, fill):
    return f'<path d="{FOLDER}" fill="{fill}" stroke="{stroke}"/>'


def folder_open(stroke, fill):
    return (f'<path d="{FOLDER_OPEN_BACK}" fill="{fill}" stroke="{stroke}" stroke-linejoin="round"/>'
            f'<path d="{FOLDER_OPEN_FRONT}" fill="{fill}" stroke="{stroke}" stroke-linejoin="round"/>')


def badge(text, color, bg):
    """Rounded tinted tile with a bold label — the language-badge look in the screenshot."""
    n = len(text)
    size = {1: 9, 2: 7.6, 3: 6.2, 4: 5.2}.get(n, 4.6)
    width = {1: None, 2: 10.6, 3: 12.6, 4: 13.4}.get(n, 13.6)
    tl = f' textLength="{width}" lengthAdjust="spacingAndGlyphs"' if width else ""
    return (f'<rect x="0.5" y="2.5" width="15" height="11" rx="2.5" fill="{bg}" stroke="{color}" stroke-opacity=".35"/>'
            f'<text x="8" y="8.15" fill="{color}" font-family="{FONT}" font-size="{size}" font-weight="800" '
            f'text-anchor="middle" dominant-baseline="central"{tl}>{text}</text>')


def doc(stroke=GRAY, fill="#FFFFFF", extra=""):
    return (f'<path d="{DOC}" fill="{fill}" stroke="{stroke}" stroke-linejoin="round"/>'
            f'<path d="{DOC_FOLD}" stroke="{stroke}" stroke-linejoin="round"/>{extra}')


# Folders ---------------------------------------------------------------------
folders = {
    "folder": (GRAY, GRAY_BG),
    "folder-source": (BLUE, BLUE_BG),
    "folder-test": (GREEN, GREEN_BG),
    "folder-resource": (YELLOW, YELLOW_BG),
    "folder-excluded": (ORANGE, ORANGE_BG),
}
for name, (s, f) in folders.items():
    write(name, folder(s, f))
    write(name + "-open", folder_open(s, f))

# Root folder = folder with a small module square (like IntelliJ project root)
root_mark = f'<rect x="9.5" y="8.5" width="4" height="4" rx="1" fill="{BLUE}"/>'
write("folder-root", folder(GRAY, GRAY_BG) + root_mark)
write("folder-root-open", folder_open(GRAY, GRAY_BG) + root_mark)

# Language badges -------------------------------------------------------------
badges = {
    "php": ("PHP", INDIGO, INDIGO_BG),
    "blade": ("BL", ORANGE, ORANGE_BG),
    "json": ("JSON", PURPLE, PURPLE_BG),
    "js": ("JS", YELLOW, YELLOW_BG),
    "jsx": ("JSX", TEAL, TEAL_BG),
    "ts": ("TS", BLUE, BLUE_BG),
    "tsx": ("TSX", TEAL, TEAL_BG),
    "vue": ("VUE", GREEN, GREEN_BG),
    "html": ("HTML", ORANGE, ORANGE_BG),
    "css": ("CSS", BLUE, BLUE_BG),
    "scss": ("SCSS", RED, RED_BG),
    "less": ("LESS", INDIGO, INDIGO_BG),
    "markdown": ("MD", GRAY, GRAY_BG),
    "yaml": ("YML", RED, RED_BG),
    "toml": ("TOML", GRAY, GRAY_BG),
    "xml": ("XML", ORANGE, ORANGE_BG),
    "sql": ("SQL", BLUE, BLUE_BG),
    "python": ("PY", BLUE, BLUE_BG),
    "java": ("JAVA", ORANGE, ORANGE_BG),
    "kotlin": ("KT", PURPLE, PURPLE_BG),
    "go": ("GO", TEAL, TEAL_BG),
    "ruby": ("RB", RED, RED_BG),
    "rust": ("RS", ORANGE, ORANGE_BG),
    "c": ("C", BLUE, BLUE_BG),
    "cpp": ("C++", BLUE, BLUE_BG),
    "csharp": ("C#", PURPLE, PURPLE_BG),
    "header": ("H", PURPLE, PURPLE_BG),
    "swift": ("SW", ORANGE, ORANGE_BG),
    "dart": ("DT", TEAL, TEAL_BG),
    "csv": ("CSV", GREEN, GREEN_BG),
    "ini": ("INI", GRAY, GRAY_BG),
    "graphql": ("GQL", PURPLE, PURPLE_BG),
    "twig": ("TW", GREEN, GREEN_BG),
    "neon": ("NEON", GREEN, GREEN_BG),
}
for name, (t, c, b) in badges.items():
    write(name, badge(t, c, b))

# Glyph icons -----------------------------------------------------------------
write("file", doc())
write("text", doc(extra=f'<path d="M5.5 7.5h5M5.5 9.5h5M5.5 11.5h3" stroke="{GRAY}" stroke-linecap="round"/>'))
write("log", doc(extra=f'<path d="M5.5 7.5h5M5.5 9.5h5M5.5 11.5h5" stroke="{GRAY}" stroke-linecap="round" stroke-dasharray="1.6 1"/>'))
write("license", doc(extra=f'<circle cx="8" cy="8.5" r="2" stroke="{YELLOW}"/><path d="m7 10.3-.6 2.2 1.6-.8 1.6.8-.6-2.2" stroke="{YELLOW}" stroke-linejoin="round"/>'))
write("ignore", doc(extra=f'<circle cx="8" cy="9.5" r="2.5" stroke="{GRAY}"/><path d="m6.3 11.2 3.4-3.4" stroke="{GRAY}"/>'))
write("git", doc(extra=f'<circle cx="6.5" cy="7.5" r="1" fill="{ORANGE}"/><circle cx="6.5" cy="12" r="1" fill="{ORANGE}"/><circle cx="10" cy="9" r="1" fill="{ORANGE}"/><path d="M6.5 8.5v2.5M10 10c0 1-1.2 1.5-2.6 1.8" stroke="{ORANGE}"/>'))
# padlock (.env, lock files) – matches the .env glyph in the screenshot
write("lock", f'<rect x="3.5" y="7" width="9" height="7.5" rx="1.5" fill="{GRAY_BG}" stroke="{GRAY}"/>'
              f'<path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" stroke="{GRAY}"/><path d="M8 10v2" stroke="{GRAY}" stroke-linecap="round"/>')
write("env", f'<rect x="3.5" y="7" width="9" height="7.5" rx="1.5" fill="{GRAY_BG}" stroke="{GRAY}"/>'
             f'<path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" stroke="{GRAY}"/><circle cx="8" cy="10.75" r="1" fill="{GRAY}"/>')
# terminal (artisan, shell scripts) – matches the artisan glyph in the screenshot
write("terminal", f'<rect x="1.5" y="2.5" width="13" height="11" rx="1.5" fill="#FFFFFF" stroke="{GRAY}"/>'
                  f'<path d="m4.5 6 2 2-2 2M8 10.5h3.5" stroke="{GRAY}" stroke-linecap="round" stroke-linejoin="round"/>')
write("console", f'<rect x="1.5" y="2.5" width="13" height="11" rx="1.5" fill="{GRAY_BG}" stroke="{GRAY}"/>'
                 f'<path d="m4.5 6 2 2-2 2M8 10.5h3.5" stroke="{GRAY}" stroke-linecap="round" stroke-linejoin="round"/>')
write("settings", f'<path d="M7 1.5h2l.4 1.9 1.3.6 1.6-1.1 1.4 1.4-1.1 1.6.6 1.3 1.9.4v2l-1.9.4-.6 1.3 1.1 1.6-1.4 1.4-1.6-1.1-1.3.6L9 14.5H7l-.4-1.9-1.3-.6-1.6 1.1-1.4-1.4 1.1-1.6-.6-1.3L.9 9V7l1.9-.4.6-1.3-1.1-1.6 1.4-1.4 1.6 1.1 1.3-.6z" fill="{GRAY_BG}" stroke="{GRAY}" stroke-linejoin="round"/><circle cx="8" cy="8" r="2" fill="#FFFFFF" stroke="{GRAY}"/>')
write("image", f'<rect x="1.5" y="2.5" width="13" height="11" rx="1.5" fill="{TEAL_BG}" stroke="{TEAL}"/>'
               f'<circle cx="5.5" cy="6" r="1.2" fill="{TEAL}"/><path d="m2 12 3.5-3.5 2.5 2.5 2-2 3.5 3.5" stroke="{TEAL}" stroke-linejoin="round"/>')
write("svg", f'<rect x="1.5" y="2.5" width="13" height="11" rx="1.5" fill="{ORANGE_BG}" stroke="{ORANGE}"/>'
             f'<path d="M4 11 8 5l4 6z" stroke="{ORANGE}" stroke-linejoin="round"/><circle cx="8" cy="5" r="1" fill="{ORANGE}"/><circle cx="4" cy="11" r="1" fill="{ORANGE}"/><circle cx="12" cy="11" r="1" fill="{ORANGE}"/>')
write("archive", f'<rect x="2.5" y="1.5" width="11" height="13" rx="1.5" fill="{GRAY_BG}" stroke="{GRAY}"/>'
                 f'<path d="M8 1.5v1h-1v1h1v1h-1v1h1v1" stroke="{YELLOW}"/><rect x="6.5" y="8" width="3" height="3" rx=".5" stroke="{YELLOW}"/>')
write("docker", f'<rect x="2.5" y="7.5" width="3" height="3" stroke="{BLUE}"/><rect x="5.5" y="7.5" width="3" height="3" stroke="{BLUE}"/><rect x="8.5" y="7.5" width="3" height="3" stroke="{BLUE}"/><rect x="5.5" y="4.5" width="3" height="3" stroke="{BLUE}"/>'
                f'<path d="M1.5 10.5h13c0 2-1.8 3-4 3h-5c-2.2 0-4-1-4-3z" fill="{BLUE_BG}" stroke="{BLUE}" stroke-linejoin="round"/>')
write("database", f'<ellipse cx="8" cy="4" rx="5.5" ry="2" fill="{BLUE_BG}" stroke="{BLUE}"/><path d="M2.5 4v8c0 1.1 2.46 2 5.5 2s5.5-.9 5.5-2V4M2.5 8c0 1.1 2.46 2 5.5 2s5.5-.9 5.5-2" stroke="{BLUE}"/>')
write("test", f'<path d="{DOC}" fill="{GREEN_BG}" stroke="{GREEN}" stroke-linejoin="round"/><path d="{DOC_FOLD}" stroke="{GREEN}"/><path d="m5.5 9.5 1.8 1.8 3.2-3.6" stroke="{GREEN}" stroke-linecap="round" stroke-linejoin="round"/>')
write("composer", badge("JSON", PURPLE, PURPLE_BG))
write("phpunit", f'<path d="{DOC}" fill="{INDIGO_BG}" stroke="{INDIGO}" stroke-linejoin="round"/><path d="{DOC_FOLD}" stroke="{INDIGO}"/><path d="m5.5 9.5 1.8 1.8 3.2-3.6" stroke="{GREEN}" stroke-linecap="round" stroke-linejoin="round"/>')
write("font", doc(extra=f'<path d="M5.5 12.5 8 6.5l2.5 6M6.4 10.5h3.2" stroke="{GRAY}" stroke-linejoin="round"/>'))
write("pdf", badge("PDF", RED, RED_BG))
write("readme", f'<path d="{DOC}" fill="{BLUE_BG}" stroke="{BLUE}" stroke-linejoin="round"/><path d="{DOC_FOLD}" stroke="{BLUE}"/><path d="M8 7v.01M8 9v3" stroke="{BLUE}" stroke-linecap="round" stroke-width="1.3"/>')

# Icon theme definition -----------------------------------------------------
all_icons = sorted(f[:-4] for f in os.listdir(ICON_DIR))
defs = {f"_{n}": {"iconPath": f"./files/{n}.svg"} for n in all_icons}

ext = {
    "php": "php", "phtml": "php", "inc": "php",
    "blade.php": "blade", "twig": "twig", "html.twig": "twig", "neon": "neon",
    "json": "json", "jsonc": "json", "json5": "json", "webmanifest": "json",
    "js": "js", "mjs": "js", "cjs": "js", "jsx": "jsx", "ts": "ts", "mts": "ts", "cts": "ts", "d.ts": "ts", "tsx": "tsx",
    "vue": "vue", "html": "html", "htm": "html", "css": "css", "scss": "scss", "sass": "scss", "less": "less",
    "md": "markdown", "mdx": "markdown", "markdown": "markdown",
    "yml": "yaml", "yaml": "yaml", "toml": "toml", "xml": "xml", "xsd": "xml", "dist": "xml",
    "sql": "sql", "sqlite": "database", "db": "database", "py": "python", "java": "java", "kt": "kotlin", "kts": "kotlin",
    "go": "go", "rb": "ruby", "rs": "rust", "c": "c", "cpp": "cpp", "cc": "cpp", "hpp": "header", "h": "header",
    "cs": "csharp", "swift": "swift", "dart": "dart", "csv": "csv", "tsv": "csv", "ini": "ini", "conf": "settings", "cfg": "settings",
    "graphql": "graphql", "gql": "graphql",
    "sh": "terminal", "bash": "terminal", "zsh": "terminal", "fish": "terminal", "bat": "terminal", "cmd": "terminal", "ps1": "terminal",
    "txt": "text", "log": "log", "lock": "lock", "env": "env",
    "png": "image", "jpg": "image", "jpeg": "image", "gif": "image", "webp": "image", "ico": "image", "bmp": "image", "avif": "image",
    "svg": "svg", "zip": "archive", "tar": "archive", "gz": "archive", "tgz": "archive", "rar": "archive", "7z": "archive", "phar": "archive",
    "pdf": "pdf", "woff": "font", "woff2": "font", "ttf": "font", "otf": "font", "eot": "font",
    "test.php": "test", "test.ts": "test", "test.js": "test", "spec.ts": "test", "spec.js": "test",
}
names = {
    "artisan": "terminal", "composer.json": "composer", "composer.lock": "lock", "package-lock.json": "lock",
    "yarn.lock": "lock", "pnpm-lock.yaml": "lock", "bun.lockb": "lock",
    ".env": "env", ".env.example": "env", ".env.local": "env", ".env.testing": "env", ".env.production": "env",
    ".gitignore": "ignore", ".gitattributes": "git", ".gitkeep": "git", ".gitmodules": "git",
    ".dockerignore": "ignore", ".npmignore": "ignore", ".prettierignore": "ignore", ".eslintignore": "ignore",
    ".editorconfig": "settings", ".prettierrc": "settings", ".eslintrc": "settings", ".eslintrc.json": "settings",
    ".styleci.yml": "settings", "pint.json": "settings", "phpstan.neon": "settings", "phpstan.neon.dist": "settings",
    "dockerfile": "docker", "docker-compose.yml": "docker", "docker-compose.yaml": "docker", "compose.yml": "docker", "compose.yaml": "docker",
    "phpunit.xml": "phpunit", "phpunit.xml.dist": "phpunit", "pest.php": "phpunit",
    "readme.md": "readme", "readme": "readme", "license": "license", "license.md": "license", "licence": "license",
    "makefile": "terminal", "procfile": "terminal", "vite.config.js": "settings", "vite.config.ts": "settings",
    "tailwind.config.js": "settings", "webpack.mix.js": "settings", "tsconfig.json": "settings", "jsconfig.json": "settings",
}
folder_names = {
    "node_modules": "folder-excluded", "vendor": "folder-excluded", "dist": "folder-excluded", "build": "folder-excluded",
    "out": "folder-excluded", ".next": "folder-excluded", ".nuxt": "folder-excluded", "coverage": "folder-excluded",
    ".idea": "folder-excluded", ".phpunit.cache": "folder-excluded",
}
langs = {
    "php": "php", "blade": "blade", "json": "json", "jsonc": "json", "javascript": "js", "javascriptreact": "jsx",
    "typescript": "ts", "typescriptreact": "tsx", "vue": "vue", "html": "html", "css": "css", "scss": "scss", "less": "less",
    "markdown": "markdown", "yaml": "yaml", "xml": "xml", "sql": "sql", "python": "python", "java": "java", "go": "go",
    "ruby": "ruby", "rust": "rust", "c": "c", "cpp": "cpp", "csharp": "csharp", "shellscript": "terminal",
    "dockerfile": "docker", "ini": "ini", "properties": "settings", "plaintext": "text", "log": "log",
    "dotenv": "env", "ignore": "ignore", "twig": "twig", "graphql": "graphql", "dart": "dart", "swift": "swift", "kotlin": "kotlin",
}

theme = {
    "hidesExplorerArrows": False,
    "iconDefinitions": defs,
    "file": "_file",
    "folder": "_folder",
    "folderExpanded": "_folder-open",
    "rootFolder": "_folder-root",
    "rootFolderExpanded": "_folder-root-open",
    "fileExtensions": {k: f"_{v}" for k, v in ext.items()},
    "fileNames": {k: f"_{v}" for k, v in names.items()},
    "folderNames": {k: f"_{v}" for k, v in folder_names.items()},
    "folderNamesExpanded": {k: f"_{v}-open" for k, v in folder_names.items()},
    "languageIds": {k: f"_{v}" for k, v in langs.items()},
}
for m in [theme["fileExtensions"], theme["fileNames"], theme["languageIds"], theme["folderNames"], theme["folderNamesExpanded"]]:
    for v in m.values():
        assert v in defs, v
with open(os.path.join(OUT, "icons", "intellij-light-file-icons.json"), "w") as f:
    json.dump(theme, f, indent=2)
print(len(all_icons), "icons")
