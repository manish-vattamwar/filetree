# Changelog

All notable changes to FileTree will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-04-27

### Added
- Recursive directory tree walking with box-drawing characters (`├──`, `└──`, `│`)
- 40+ file-type icons mapped to extensions and filenames
- Color output via `rich` (folders = blue, symlinks = cyan, executables = green)
- `.gitignore` parsing via `pathspec` — ignored files are skipped by default
- `--all` / `-a` — show hidden dotfiles
- `--depth N` / `-d N` — limit recursion depth
- `--dirs-only` / `-D` — only show directories
- `--size` / `-s` — human-readable file sizes (B, KB, MB, GB)
- `--modified` / `-m` — last-modified timestamps
- `--permissions` / `-p` — Unix rwx permissions string
- `--sort name|size|date` — sort entries within directories
- `--exclude PATTERN` — glob-based exclusion (repeatable)
- `--include PATTERN` — show only matching files (repeatable)
- `--find PATTERN` / `-f PATTERN` — find files in tree context
- `--no-icons` — disable all icons
- `--no-color` — disable ANSI colors (also auto-disabled when piping)
- `--json` — export tree as JSON
- `--markdown` — export tree as Markdown list
- `--html` — export tree as collapsible HTML page
- `--clipboard` — copy output to clipboard via `pyperclip`
- `--output FILE` / `-o FILE` — write output to a file
- `--git` / `-g` — show git status icons (❓ untracked, ✏️ modified, ✨ added, 🗑️ deleted)
- `--stats` — display top file types by size
- `--interactive` / `-i` — full-screen TUI using Textual (↑↓ navigate, e expand all, c collapse all)
- `--completions bash|zsh|fish` — print shell completion scripts
- `~/.filetreerc` config file (JSON) for persisting default options
- `pytest` test suite covering CLI, walker, renderer, and icons
- MIT license
