# Contributing to FileTree

Thank you for your interest in contributing to FileTree! 🌳

## How to Contribute

### Reporting Bugs
- Search [existing issues](../../issues) first to avoid duplicates.
- Use the **Bug Report** issue template.
- Include your OS, Python version, and terminal info.

### Suggesting Features
- Use the **Feature Request** issue template.
- Explain the use case clearly — why would this benefit users?

### Submitting Pull Requests

1. **Fork** the repository and create a branch from `main`:
   ```bash
   git checkout -b feat/my-new-feature
   ```

2. **Set up** the dev environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Make your changes** and write tests for new behaviour.

4. **Run the test suite** — it must pass:
   ```bash
   pytest
   ```

5. **Lint and format** your code:
   ```bash
   ruff check . --fix
   ruff format .
   ```

6. **Commit** with a clear message following [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: add --watch mode for live tree updates
   fix: respect .gitignore in symlinked dirs
   docs: add fish completion instructions
   ```

7. **Open a Pull Request** — fill in the PR template.

## Project Structure

```
src/filetree/
├── cli.py        — Click CLI, all flags and options
├── walker.py     — Recursive directory walker
├── renderer.py   — Rich-based tree rendering
├── icons.py      — Icon registry (extension → emoji)
├── colors.py     — Rich theme / styles
├── config.py     — ~/.filetreerc loader
├── tui.py        — Textual interactive TUI
├── utils.py      — Size/time/permission formatters
└── exporters/    — JSON, Markdown, HTML exporters
```

## Code Style

- Python 3.10+ type hints throughout.
- `ruff` for linting and formatting (line length 100).
- Keep functions small and focused.
- New icons? Add them in `icons.py` — both `EXTENSION_ICONS` and `FILENAME_ICONS`.

## Areas Needing Help

- 🎯 Nerd Font icon set with auto-detection
- 🎯 `--watch` mode (live reload using `watchdog`)
- 🎯 Diff mode — compare two directory trees
- 🎯 More tests (coverage is always welcome)
- 🎯 Windows testing and compatibility fixes

## Questions?

Open a [Discussion](../../discussions) — happy to help!
