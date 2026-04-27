"""
Tree rendering engine.
"""

from typing import List
from pathlib import Path
from rich.console import Console
from rich.text import Text
from rich.table import Table

from filetree.walker import TreeNode, TreeWalker
from filetree.icons import get_icon
from filetree.utils import format_size, format_time, format_permissions

# Tree characters
TEE = "├── "
LAST_CHILD = "└── "
PIPE = "│   "
SPACE = "    "

def get_git_icon(status_code: str) -> str:
    if not status_code:
        return ""
    if status_code == "??":
        return "❓"
    if status_code.startswith("M") or status_code.endswith("M"):
        return "✏️"
    if status_code.startswith("A"):
        return "✨"
    if status_code.startswith("D") or status_code.endswith("D"):
        return "🗑️"
    return "📝"

class TreeRenderer:
    def __init__(self, console: Console, show_icons: bool = True, show_size: bool = False, show_modified: bool = False, show_permissions: bool = False, show_git: bool = False, show_stats: bool = False):
        self.console = console
        self.show_icons = show_icons
        self.show_size = show_size
        self.show_modified = show_modified
        self.show_permissions = show_permissions
        self.show_git = show_git
        self.show_stats = show_stats

    def render(self, root_path: str, walker: TreeWalker):
        table = Table(show_header=False, box=None, padding=(0, 1), collapse_padding=True)
        
        if self.show_git:
            table.add_column("Git", justify="center")
            
        table.add_column("Tree", no_wrap=True)
        
        if self.show_permissions:
            table.add_column("Permissions", style="magenta")
        if self.show_size:
            table.add_column("Size", style="cyan", justify="right")
        if self.show_modified:
            table.add_column("Modified", style="yellow")
            
        root_name = Path(root_path).resolve().name or "."
        
        # Build root row
        root_text = self._build_name_text(root_name, is_dir=True, is_symlink=False)
        
        row = []
        if self.show_git:
            row.append("") # Root dir git status usually empty
            
        row.append(root_text)
        
        try:
            st = Path(root_path).resolve().stat()
            if self.show_permissions:
                row.append(format_permissions(st.st_mode))
            if self.show_size:
                row.append(format_size(st.st_size))
            if self.show_modified:
                row.append(format_time(st.st_mtime))
        except OSError:
            if self.show_permissions:
                row.append("")
            if self.show_size:
                row.append("")
            if self.show_modified:
                row.append("")
            
        table.add_row(*row)

        nodes = walker.walk()
        if nodes:
            self._render_nodes(table, nodes, [])
            
        self.console.print(table)
        self._print_summary(walker, nodes)

    def _build_name_text(self, name: str, is_dir: bool, is_symlink: bool, is_exec: bool = False) -> Text:
        if is_symlink:
            style = "tree.symlink"
        elif is_dir:
            style = "tree.dir"
        else:
            style = "tree.exec" if is_exec else "tree.file"
            
        if self.show_icons:
            icon = get_icon(name, is_dir=is_dir, is_symlink=is_symlink)
            return Text(f"{icon} {name}", style=style)
        else:
            return Text(name, style=style)

    def _render_nodes(self, table: Table, nodes: List[TreeNode], prefixes: List[str]):
        for i, node in enumerate(nodes):
            is_last = (i == len(nodes) - 1)
            
            prefix_str = "".join(prefixes)
            branch = LAST_CHILD if is_last else TEE
            
            import os
            is_exec = os.access(node.entry.path, os.X_OK) and not node.entry.is_dir
            
            line_text = Text(prefix_str + branch, style="tree.line")
            name_text = self._build_name_text(node.entry.name, node.entry.is_dir, node.entry.is_symlink, is_exec)
            
            tree_col = line_text + name_text
            
            row = []
            if self.show_git:
                row.append(get_git_icon(node.entry.git_status))
                
            row.append(tree_col)
            
            if self.show_permissions:
                row.append(format_permissions(node.entry.mode))
            if self.show_size:
                row.append(format_size(node.entry.size))
            if self.show_modified:
                row.append(format_time(node.entry.mtime))
                
            table.add_row(*row)
            
            if node.children:
                new_prefixes = prefixes.copy()
                new_prefixes.append(SPACE if is_last else PIPE)
                self._render_nodes(table, node.children, new_prefixes)

    def _print_summary(self, walker: TreeWalker, nodes: List[TreeNode] = None):
        dirs = walker.total_dirs
        files = walker.total_files
        dir_text = f"{dirs} director{'y' if dirs == 1 else 'ies'}"
        file_text = f"{files} file{'s' if files != 1 else ''}"
        
        if walker.dirs_only:
            self.console.print(f"\n{dir_text}")
        else:
            self.console.print(f"\n{dir_text}, {file_text}")

        if self.show_stats and nodes:
            self.console.print("\n[bold cyan]📊 Repository Stats[/bold cyan]")
            ext_sizes = {}
            def walk_stats(nodes_list):
                for node in nodes_list:
                    if not node.entry.is_dir:
                        ext = Path(node.entry.name).suffix.lower()
                        if not ext:
                            ext = "no extension"
                        ext_sizes[ext] = ext_sizes.get(ext, 0) + node.entry.size
                    walk_stats(node.children)
            walk_stats(nodes)
            
            sorted_exts = sorted(ext_sizes.items(), key=lambda x: x[1], reverse=True)[:5]
            if sorted_exts:
                self.console.print("  [bold]Top 5 Types by Size:[/bold]")
                for ext, size in sorted_exts:
                    self.console.print(f"    {ext.ljust(15)} {format_size(size)}")
