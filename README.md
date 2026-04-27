# 🌳 FileTree

> **See your project at a glance.** An open-source CLI tool that beautifully renders your directory structure with icons, right in the terminal.

[![PyPI version](https://badge.fury.io/py/filetree-cli.svg)](https://badge.fury.io/py/filetree-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/manish-vattamwar/filetree/actions/workflows/ci.yml/badge.svg)](https://github.com/manish-vattamwar/filetree/actions/workflows/ci.yml)

---

## ✨ Features

- 🌲 **Beautiful tree rendering** — box-drawing characters (`├──`, `└──`, `│`)
- 🎨 **40+ file-type icons** — Python 🐍, JavaScript 🟨, Rust 🦀, Docker 🐳, and more
- 🎨 **Color output** — folders, symlinks, and executables are distinctly colored
- 🙈 **`.gitignore` aware** — automatically skips ignored files
- 🔀 **Git status** — see modified ✏️, untracked ❓, staged ✨ files at a glance
- 📊 **Stats mode** — top file types by size
- 🖱️ **Interactive TUI** — navigate your tree with arrow keys
- 📤 **Export to JSON, Markdown, HTML** — perfect for README generation
- ⚙️ **Config file** — persist your defaults in `~/.filetreerc`
- 🐚 **Shell completions** — bash, zsh, and fish

---

## 📦 Installation

```bash
pip install filetree-cli
```

---

## 🚀 Quick Start

```bash
# Show current directory
filetree .

# Show hidden files
filetree . -a

# Show with sizes, timestamps, and permissions
filetree . -s -m -p

# Show git status
filetree . -g

# Interactive TUI mode
filetree . -i
```

---

## 📖 Usage

```
Usage: filetree [OPTIONS] [PATH]

  🌳 Display directory structure with icons.

Arguments:
  PATH    Root directory to display [default: .]

Options:
  -a, --all            Show hidden files
  -d, --depth N        Max display depth
  -D, --dirs-only      Only show directories
  -f, --find PATTERN   Find files matching glob (repeatable)
  --exclude PATTERN    Exclude glob pattern (repeatable)
  --include PATTERN    Include only matching (repeatable)
  -s, --size           Show file sizes
  -m, --modified       Show modification times
  -p, --permissions    Show file permissions
  -g, --git            Show git status icons
  --stats              Show repo stats (top file types by size)
  --sort TYPE          Sort by: name, size, date [default: name]
  --no-icons           Disable icons
  --no-color           Disable colors
  --json               Output as JSON
  --markdown           Output as Markdown
  --html               Output as collapsible HTML
  --clipboard          Copy output to clipboard
  -o, --output FILE    Write to file
  -i, --interactive    Interactive TUI mode
  --completions SHELL  Print shell completions (bash/zsh/fish)
  -v, --version        Show version
  -h, --help           Show this help
```

---

## 🖼️ Example Output

```
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

3 directories, 10 files
```

---

## ⚙️ Config File

Create `~/.filetreerc` (JSON) to set defaults:

```json
{
  "all": false,
  "size": true,
  "modified": true,
  "git": true,
  "sort": "name",
  "no_icons": false,
  "exclude": ["*.pyc", "__pycache__"]
}
```

---

## 🐚 Shell Completions

```bash
# Bash
filetree --completions bash >> ~/.bashrc && source ~/.bashrc

# Zsh
filetree --completions zsh >> ~/.zshrc && source ~/.zshrc

# Fish
filetree --completions fish > ~/.config/fish/completions/filetree.fish
```

---

## 📤 Export Examples

```bash
# Export as Markdown (great for README.md!)
filetree . --markdown

# Export as interactive HTML
filetree . --html -o tree.html

# Export as JSON for scripting
filetree . --json -o tree.json

# Copy to clipboard
filetree . --markdown --clipboard
```

---

## 🛠️ Development

```bash
git clone https://github.com/yourusername/filetree.git
cd filetree
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run during development
filetree .

# Run tests
pytest

# Lint & format
ruff check . --fix && ruff format .
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

## 📜 License

[MIT](LICENSE) © Manish
