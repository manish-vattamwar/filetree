"""
CLI entry point for FileTree.
"""

import click
from rich.console import Console
from pathlib import Path
import sys

from filetree.walker import TreeWalker
from filetree.renderer import TreeRenderer
from filetree.colors import filetree_theme
from filetree.config import load_config
from filetree.exporters import export_json, export_markdown, export_html
from filetree import __version__


def get_default_config():
    return load_config()


SHELL_COMPLETIONS = {
    "bash": '''\
_filetree_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local opts="-a --all -d --depth -D --dirs-only --exclude --include -f --find
                -s --size -m --modified -p --permissions -g --git --stats
                --sort --no-icons --no-color --json --markdown --html
                --clipboard -o --output -i --interactive -v --version -h --help"
    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
    if [[ "$cur" != -* ]]; then
        COMPREPLY+=( $(compgen -d -- "${cur}") )
    fi
}
complete -F _filetree_completion filetree
''',
    "zsh": '''\
#compdef filetree

_filetree() {
    local -a args
    args=(
        '(-a --all)'{-a,--all}'[Show hidden files]'
        '(-d --depth)'{-d,--depth}'[Max display depth]:depth:'
        '(-D --dirs-only)'{-D,--dirs-only}'[Only show directories]'
        '--exclude[Exclude glob pattern]:pattern:'
        '--include[Include only matching]:pattern:'
        '(-f --find)'{-f,--find}'[Find matching files]:pattern:'
        '(-s --size)'{-s,--size}'[Show file sizes]'
        '(-m --modified)'{-m,--modified}'[Show modification times]'
        '(-p --permissions)'{-p,--permissions}'[Show file permissions]'
        '(-g --git)'{-g,--git}'[Show git status icons]'
        '--stats[Show stats mode]'
        '--sort[Sort by]:sort:(name size date)'
        '--no-icons[Disable icons]'
        '--no-color[Disable color output]'
        '--json[Output as JSON]'
        '--markdown[Output as Markdown]'
        '--html[Output as HTML]'
        '--clipboard[Copy to clipboard]'
        '(-o --output)'{-o,--output}'[Write to file]:file:_files'
        '(-i --interactive)'{-i,--interactive}'[Interactive TUI mode]'
        '(-v --version)'{-v,--version}'[Show version]'
        '(-h --help)'{-h,--help}'[Show help]'
        ':path:_files -/'
    )
    _arguments -s $args
}

_filetree
''',
    "fish": '''\
# filetree completions for fish shell
complete -c filetree -s a -l all         -d "Show hidden files"
complete -c filetree -s d -l depth       -d "Max display depth" -r
complete -c filetree -s D -l dirs-only   -d "Only show directories"
complete -c filetree      -l exclude     -d "Exclude glob pattern" -r
complete -c filetree      -l include     -d "Include only matching" -r
complete -c filetree -s f -l find        -d "Find matching files" -r
complete -c filetree -s s -l size        -d "Show file sizes"
complete -c filetree -s m -l modified    -d "Show modification times"
complete -c filetree -s p -l permissions -d "Show file permissions"
complete -c filetree -s g -l git         -d "Show git status icons"
complete -c filetree      -l stats       -d "Show stats mode"
complete -c filetree      -l sort        -d "Sort entries" -r -a "name size date"
complete -c filetree      -l no-icons    -d "Disable icons"
complete -c filetree      -l no-color    -d "Disable color output"
complete -c filetree      -l json        -d "Output as JSON"
complete -c filetree      -l markdown    -d "Output as Markdown"
complete -c filetree      -l html        -d "Output as HTML"
complete -c filetree      -l clipboard   -d "Copy output to clipboard"
complete -c filetree -s o -l output      -d "Write output to file" -r -F
complete -c filetree -s i -l interactive -d "Interactive TUI mode"
complete -c filetree -s v -l version     -d "Show version"
complete -c filetree -s h -l help        -d "Show help"
complete -c filetree -a "(__fish_complete_directories)" -d "Directory"
''',
}


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("-a", "--all", "all_files", is_flag=True, help="Show hidden files")
@click.option("-d", "--depth", type=int, help="Max display depth")
@click.option("-D", "--dirs-only", is_flag=True, help="Only show directories")
@click.option("--exclude", multiple=True, help="Exclude glob pattern (repeatable)")
@click.option("--include", multiple=True, help="Include only matching (repeatable)")
@click.option("-f", "--find", multiple=True, help="Find files matching glob, show in context")
@click.option("-s", "--size", is_flag=True, help="Show file sizes")
@click.option("-m", "--modified", is_flag=True, help="Show modification times")
@click.option("-p", "--permissions", is_flag=True, help="Show file permissions")
@click.option("-g", "--git", is_flag=True, help="Show git status icons")
@click.option("--stats", is_flag=True, help="Show repo stats (top file types by size)")
@click.option("--sort", "sort_by", type=click.Choice(["name", "size", "date"], case_sensitive=False), default="name", help="Sort entries by name/size/date")
@click.option("--no-icons", is_flag=True, help="Disable icons")
@click.option("--no-color", is_flag=True, help="Disable color output")
@click.option("--json", "json_export", is_flag=True, help="Output as JSON")
@click.option("--markdown", is_flag=True, help="Output as Markdown")
@click.option("--html", is_flag=True, help="Output as collapsible HTML")
@click.option("--clipboard", is_flag=True, help="Copy output to clipboard")
@click.option("-o", "--output", "output_file", type=click.Path(), help="Write output to file")
@click.option("-i", "--interactive", is_flag=True, help="Interactive TUI mode (navigate with arrow keys)")
@click.option("--completions", type=click.Choice(["bash", "zsh", "fish"]), help="Print shell completions and exit")
@click.version_option(version=__version__, prog_name="filetree")
def cli(path, all_files, depth, dirs_only, exclude, include, find, size, modified,
        permissions, git, stats, sort_by, no_icons, no_color, json_export, markdown,
        html, clipboard, output_file, interactive, completions):
    """🌳 Display directory structure with icons."""

    # Shell completions shortcut
    if completions:
        print(SHELL_COMPLETIONS[completions])
        return

    config = get_default_config()

    if not all_files:
        all_files = config.get("all", False)
    if not dirs_only:
        dirs_only = config.get("dirs_only", False)
    if not size:
        size = config.get("size", False)
    if not modified:
        modified = config.get("modified", False)
    if not permissions:
        permissions = config.get("permissions", False)
    if not git:
        git = config.get("git", False)
    if not stats:
        stats = config.get("stats", False)
    if not interactive:
        interactive = config.get("interactive", False)
    if sort_by == "name" and "sort" in config:
        sort_by = config.get("sort", "name")
    if not no_icons:
        no_icons = config.get("no_icons", False)
    if not no_color:
        no_color = config.get("no_color", False)

    exclude_list = list(exclude) + config.get("exclude", [])
    include_list = list(include) + list(find) + config.get("include", [])

    walker = TreeWalker(
        root=path,
        all_files=all_files,
        max_depth=depth,
        dirs_only=dirs_only,
        excludes=exclude_list,
        includes=include_list,
        sort_by=sort_by,
        show_git=git
    )

    # ── Interactive TUI ──────────────────────────────────────────────────────
    if interactive:
        try:
            from filetree.tui import run_tui
            run_tui(path, walker)
        except ImportError:
            click.echo("Textual is required for interactive mode: pip install textual", err=True)
        return

    root_name = Path(path).resolve().name or "."

    # ── Export modes ─────────────────────────────────────────────────────────
    export_content = None
    if json_export:
        nodes = walker.walk()
        export_content = export_json(nodes, root_name)
    elif markdown:
        nodes = walker.walk()
        export_content = export_markdown(nodes, root_name, show_icons=not no_icons)
    elif html:
        nodes = walker.walk()
        export_content = export_html(nodes, root_name, show_icons=not no_icons)

    if export_content is not None:
        _write_or_clip(export_content, clipboard, output_file)
        return

    # ── Normal terminal render ────────────────────────────────────────────────
    is_tty = sys.stdout.isatty()
    color_system = None if (no_color or not is_tty) else "auto"
    console = Console(theme=filetree_theme, color_system=color_system)

    renderer_kwargs = dict(
        show_icons=not no_icons,
        show_size=size,
        show_modified=modified,
        show_permissions=permissions,
        show_git=git,
        show_stats=stats,
    )

    if clipboard or output_file:
        cap_console = Console(theme=filetree_theme, color_system=None)
        renderer = TreeRenderer(console=cap_console, **renderer_kwargs)
        with cap_console.capture() as capture:
            renderer.render(path, walker)
        _write_or_clip(capture.get(), clipboard, output_file)
    else:
        renderer = TreeRenderer(console=console, **renderer_kwargs)
        renderer.render(path, walker)


def _write_or_clip(content: str, clipboard: bool, output_file: str | None):
    if clipboard:
        try:
            import pyperclip
            pyperclip.copy(content)
            click.echo("✅ Copied to clipboard!")
        except Exception as e:
            click.echo(f"Failed to copy to clipboard: {e}", err=True)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        click.echo(f"✅ Output written to {output_file}")
    if not clipboard and not output_file:
        print(content)


if __name__ == "__main__":
    cli()
