# 🌳 FileTree — Project Plan

> **An open-source CLI tool that beautifully renders your directory structure with icons, right in the terminal.**

---

## 1. Vision & Goals

| Aspect | Detail |
|---|---|
| **Name** | `filetree` |
| **Language** | Python 3.10+ |
| **Distribution** | PyPI (`pip install filetree-cli`) + standalone binary via PyInstaller |
| **License** | MIT |
| **Tagline** | *"See your project at a glance."* |

### Core Value Proposition
- One command → full directory tree with **Nerd Font / Unicode icons** for every file type.
- Zero config by default, deeply configurable when needed.
- Fast — handles large repos without breaking a sweat.

---

## 2. Features — Phased Roadmap

### Phase 1 — MVP (v0.1.0) ✨
> Get a working CLI that prints a pretty tree.

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Recursive tree walk** | Walk the directory tree from a given root (default: `.`) |
| 2 | **Tree-line drawing** | Use box-drawing characters (`├──`, `└──`, `│`) for structure |
| 3 | **File-type icons** | Map extensions → icons (📁 folders, 🐍 `.py`, 📄 `.txt`, ⚙️ `.json`, etc.) using a built-in icon registry |
| 4 | **Color output** | Colorize folders, files, symlinks differently using `rich` or ANSI codes |
| 5 | **`.gitignore` respect** | Skip files/folders listed in `.gitignore` by default |
| 6 | **CLI argument parsing** | Use `click` for: `filetree [PATH] [OPTIONS]` |
| 7 | **`--depth N`** | Limit recursion depth |
| 8 | **`--all` / `-a`** | Show hidden files (dotfiles) |
| 9 | **`--dirs-only`** | Only show directories |
| 10 | **Summary line** | Print `X directories, Y files` at the bottom |

### Phase 2 — Power User (v0.2.0) 🔧
> Make it configurable and smarter.

| # | Feature | Description |
|---|---------|-------------|
| 11 | **`--exclude PATTERN`** | Glob-based exclusion (`--exclude "*.pyc"`) |
| 12 | **`--include PATTERN`** | Only show matching files |
| 13 | **`--size`** | Show file sizes (human-readable: KB, MB, GB) |
| 14 | **`--modified`** | Show last-modified timestamps |
| 15 | **`--permissions`** | Show Unix file permissions |
| 16 | **`--sort NAME\|SIZE\|DATE`** | Sort entries within each directory |
| 17 | **Nerd Font icons** | Detect Nerd Font support and use rich file-specific icons |
| 18 | **Config file** | `~/.filetreerc` or `.filetree.yaml` for default options |
| 19 | **`--no-icons`** | Disable icons for plain terminals |
| 20 | **`--no-color`** | Disable color output |

### Phase 3 — Export & Integration (v0.3.0) 📤
> Let people use the output elsewhere.

| # | Feature | Description |
|---|---------|-------------|
| 21 | **`--json`** | Output tree as JSON |
| 22 | **`--markdown`** | Output tree as Markdown (great for README.md!) |
| 23 | **`--html`** | Output tree as a collapsible HTML page |
| 24 | **`--clipboard`** | Copy output to clipboard |
| 25 | **`--output FILE`** | Write output to a file |
| 26 | **Pipe-friendly mode** | Auto-detect non-TTY and strip colors/icons |

### Phase 4 — Ecosystem (v1.0.0) 🚀
> Polish, community, integrations.

| # | Feature | Description |
|---|---------|-------------|
| 27 | **Interactive mode** | Navigate the tree with arrow keys (using `textual` or `curses`) |
| 28 | **Plugin system** | Let users add custom icon mappings or formatters |
| 29 | **Git integration** | Show git status icons (modified ✏️, untracked ❓, staged ✅) |
| 30 | **Search / filter** | `filetree --find "*.test.js"` highlights matching files in context |
| 31 | **Stats mode** | Show language breakdown, largest files, etc. |
| 32 | **Shell completions** | Auto-completions for bash, zsh, fish |

---

## 3. Project Structure

```
filetree/
├── 📄 README.md               # Project overview, install, usage
├── 📄 LICENSE                  # MIT License
├── 📄 GEMINI.md                # This plan
├── 📄 CHANGELOG.md             # Version history
├── 📄 pyproject.toml           # Build config (PEP 621)
├── 📄 .gitignore               # Git ignore rules
├── 📁 src/
│   └── 📁 filetree/
│       ├── 📄 __init__.py      # Package init, version
│       ├── 📄 __main__.py      # Entry point: python -m filetree
│       ├── 📄 cli.py           # Argument parsing & CLI logic
│       ├── 📄 walker.py        # Directory walking engine
│       ├── 📄 renderer.py      # Tree rendering (box chars, indentation)
│       ├── 📄 icons.py         # Icon registry (extension → icon mapping)
│       ├── 📄 colors.py        # Color/style definitions
│       ├── 📄 config.py        # Config file loading
│       ├── 📁 exporters/
│       │   ├── 📄 __init__.py
│       │   ├── 📄 json_export.py
│       │   ├── 📄 markdown_export.py
│       │   └── 📄 html_export.py
│       └── 📄 utils.py         # Helpers (size formatting, etc.)
├── 📁 tests/
│   ├── 📄 __init__.py
│   ├── 📄 test_walker.py
│   ├── 📄 test_renderer.py
│   ├── 📄 test_icons.py
│   └── 📄 test_cli.py
└── 📁 assets/
    └── 📄 demo.gif             # Terminal recording for README
```

---

## 4. Technology Choices

| Component | Choice | Why |
|---|---|---|
| **Language** | Python 3.10+ | Widely available, great for CLI tools |
| **CLI framework** | `click` | Clean decorators, auto-help, composable |
| **Terminal styling** | `rich` | Best-in-class terminal formatting, colors, emoji |
| **Gitignore parsing** | `pathspec` | Robust `.gitignore` pattern matching |
| **Testing** | `pytest` | Industry standard, simple |
| **Build system** | `pyproject.toml` + `hatchling` | Modern Python packaging |
| **Linting** | `ruff` | Fast, all-in-one linter + formatter |
| **Binary packaging** | `PyInstaller` | Cross-platform standalone builds |

---

## 5. Icon Registry Design

The icon system maps file types to Unicode/emoji icons:

```python
# icons.py — simplified example

FOLDER_ICON = "📁"
FILE_ICON = "📄"
SYMLINK_ICON = "🔗"

EXTENSION_ICONS = {
    # Languages
    ".py":    "🐍",  ".js":    "🟨",  ".ts":    "🔷",
    ".rs":    "🦀",  ".go":    "🐹",  ".java":  "☕",
    ".rb":    "💎",  ".c":     "🔵",  ".cpp":   "🔵",
    ".h":     "📋",

    # Web
    ".html":  "🌐",  ".css":   "🎨",  ".scss":  "🎨",

    # Data
    ".json":  "⚙️",  ".yaml":  "⚙️",  ".yml":   "⚙️",
    ".toml":  "⚙️",  ".xml":   "📋",  ".csv":   "📊",

    # Docs
    ".md":    "📝",  ".txt":   "📄",  ".pdf":   "📕",
    ".doc":   "📘",  ".docx":  "📘",

    # Media
    ".png":   "🖼️",  ".jpg":   "🖼️",  ".gif":   "🖼️",
    ".svg":   "🖼️",  ".mp4":   "🎬",  ".mp3":   "🎵",

    # DevOps
    ".sh":    "🐚",  ".bash":  "🐚",  ".env":   "🔒",

    # Archives
    ".zip":   "📦",  ".tar":   "📦",  ".gz":    "📦",
}

FILENAME_ICONS = {
    "Dockerfile":       "🐳",
    "Makefile":         "🔨",
    ".gitignore":       "🙈",
    "LICENSE":          "📜",
    "README.md":        "📖",
    "package.json":     "📦",
    "requirements.txt": "📋",
}
```

---

## 6. Example Output

```
$ filetree ~/projects/my-app

📁 my-app
├── 📖 README.md
├── 📜 LICENSE
├── 📦 package.json
├── 🙈 .gitignore
├── 📁 src
│   ├── 🟨 index.js
│   ├── 🟨 app.js
│   └── 📁 components
│       ├── 🟨 Header.js
│       └── 🟨 Footer.js
├── 📁 public
│   ├── 🌐 index.html
│   └── 🖼️ logo.png
└── 📁 tests
    └── 🟨 app.test.js

4 directories, 10 files
```

---

## 7. CLI Interface Design

```
Usage: filetree [OPTIONS] [PATH]

  🌳 Display directory structure with icons.

Arguments:
  PATH    Root directory to display [default: .]

Options:
  -a, --all            Show hidden files
  -d, --depth N        Max display depth
  -D, --dirs-only      Only show directories
  -s, --size           Show file sizes
  -m, --modified       Show modification times
  -p, --permissions    Show file permissions
  --sort TYPE          Sort by: name, size, date [default: name]
  --exclude PATTERN    Exclude glob pattern (repeatable)
  --include PATTERN    Include only matching (repeatable)
  --no-icons           Disable icons
  --no-color           Disable colors
  --json               Output as JSON
  --markdown           Output as Markdown
  --html               Output as HTML
  -o, --output FILE    Write to file
  -v, --version        Show version
  -h, --help           Show this help
```

---

## 8. Development Workflow

### Setup
```bash
git clone https://github.com/yourusername/filetree.git
cd filetree
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Daily Workflow
```bash
# Run during development
python -m filetree .

# Run tests
pytest

# Lint & format
ruff check . --fix
ruff format .

# Build
python -m build
```

### Release Checklist
1. Update version in `__init__.py`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Build: `python -m build`
5. Publish: `twine upload dist/*`
6. Tag: `git tag v0.x.0 && git push --tags`

---

## 9. Enhancement Ideas 💡

| # | Enhancement | Impact |
|---|-------------|--------|
| 🎯 | **Treemap visualization** — generate an SVG treemap showing file sizes | High |
| 🎯 | **`--watch` mode** — live-update the tree as files change | Medium |
| 🎯 | **Remote trees** — SSH into a server and display its tree | High |
| 🎯 | **Diff mode** — compare two directory trees side by side | High |
| 🎯 | **Custom themes** — let users define color schemes | Medium |
| 🎯 | **`.filetreeignore`** — project-specific ignore file | Low |
| 🎯 | **GitHub Action** — auto-generate tree in PR descriptions | High |
| 🎯 | **VS Code extension** — sidebar tree with the same icon set | High |
| 🎯 | **Homebrew formula** — `brew install filetree` | Medium |
| 🎯 | **Man page** — proper Unix man page | Low |
| 🎯 | **i18n** — localized output | Low |
| 🎯 | **Benchmarking** — compare speed against `tree`, `exa --tree` | Medium |

---

## 10. Open-Source Checklist

- [ ] `README.md` with install, usage, screenshots, and badges
- [ ] `CONTRIBUTING.md` with contribution guidelines
- [ ] `CODE_OF_CONDUCT.md`
- [ ] GitHub Issue templates (bug report, feature request)
- [ ] GitHub PR template
- [ ] CI/CD with GitHub Actions (lint, test, publish)
- [ ] Badges: PyPI version, downloads, license, CI status
- [ ] `demo.gif` terminal recording using `asciinema` or `vhs`
- [ ] PyPI page with rich description

---

*Plan created: 2026-04-27 | Author: Manish + Antigravity*
