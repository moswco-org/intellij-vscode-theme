# Dev Themes (Light & Dark)

A high-density, High-density, modern-IDE-inspired theme for VS Code in **light** and **dark**. Ships three parts:

| Part | Picker | What it covers |
| --- | --- | --- |
| Colour themes | *Preferences: Color Theme* → **Dev Light** / **Dev Dark** | Editor, tabs, breadcrumbs, project tree, tool strip, run/terminal panel, status bar, JetBrains syntax colours (PHP-tuned) |
| File icons | *Preferences: File Icon Theme* → **Dev File Icons** | 68 New UI–style icons, with light and dark variants that switch automatically with the colour theme: language badges (PHP, JSON, TS…), folders, `.env`/lock files, `artisan`, Docker, tests, images… |
| Product icons | *Preferences: Product Icon Theme* → **Dev Product Icons** | Tool-window strip (project, commit, search, debug, plugins), chevrons, run ▶ / stop ■, breakpoints, bell, gear, branch, window controls |

## Recommended settings

```jsonc
{
  "workbench.colorTheme": "Dev Light",
  // or follow the OS appearance:
  "window.autoDetectColorScheme": true,
  "workbench.preferredLightColorTheme": "Dev Light",
  "workbench.preferredDarkColorTheme": "Dev Dark",
  "workbench.iconTheme": "intellij-light-file-icons",
  "workbench.productIconTheme": "intellij-light-product-icons",

  "editor.fontFamily": "'JetBrains Mono', monospace",
  "editor.fontSize": 13,
  "editor.lineHeight": 22,
  "editor.fontLigatures": true,
  "editor.semanticHighlighting.enabled": true,
  "editor.glyphMargin": true,
  "editor.renderLineHighlight": "all",
  "editor.minimap.renderCharacters": false,

  "workbench.tree.indent": 14,
  "workbench.tree.renderIndentGuides": "none",
  "workbench.editor.tabActionLocation": "right",
  "workbench.editor.highlightModifiedTabs": true,
  "breadcrumbs.enabled": true,
  "window.commandCenter": true,
  "window.titleBarStyle": "custom"
}
```

## Layout

```
themes/intellij-light-ide-color-theme.json   light colour theme (JSONC, sectioned to match the IDE layout) — the source of truth
themes/intellij-dark-ide-color-theme.json    dark colour theme — generated from the light one
icons/intellij-light-file-icons.json         file icon theme
icons/files/*.svg                            file & folder icons (16×16, light)
icons/files-dark/*.svg                       dark variants
icons/intellij-product-icons.json            product icon theme
icons/intellij-product-icons.woff            product icon font
scripts/build_*.py                           generators (see Rebuilding)
```

The colour theme is split into numbered sections that follow the IDE window top to bottom:
base → title bar / Search Everywhere → tool strip → project tree → tabs → breadcrumbs → editor & gutter →
popups → bottom tool window → status bar → controls → menus → VCS → run/debug/tests → misc,
then semantic tokens and TextMate scopes.

## Rebuilding

Edit the light theme, then regenerate the dark one; the script stops if it meets a colour it has no dark mapping for.

```bash
python3 scripts/build_dark_theme.py .                                      # light theme → dark theme
python3 scripts/build_file_icons.py . && python3 scripts/build_dark_icons.py .   # file icons (light + dark)
python3 scripts/build_product_icons.py .                                   # product icon font (needs fontTools)
```

## Install locally

Copy this folder to `~/.vscode/extensions/mreromz.dev-themes`, restart VS Code and pick the three themes above.
Or press F5 in this folder to launch an Extension Development Host.

## Package

```bash
npm i -g @vscode/vsce
vsce package
```

## License & notices

MIT — see [LICENSE](LICENSE). This project is independent and is not affiliated with or endorsed by JetBrains s.r.o. "JetBrains", "IntelliJ" and "PhpStorm" are trademarks of JetBrains s.r.o.; the recommended font JetBrains Mono is a separate project under the SIL OFL.
