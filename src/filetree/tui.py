"""
Interactive TUI mode powered by Textual.

Keybindings
-----------
q / Ctrl+C  Quit
d           Toggle dark/light mode
e           Expand all
c           Collapse all
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Tree, Label
from textual.widgets.tree import TreeNode as TextualTreeNode
from pathlib import Path
from typing import List

from filetree.walker import TreeWalker, TreeNode
from filetree.icons import get_icon


class FileTreeApp(App):
    """Interactive FileTree browser."""

    TITLE = "🌳 FileTree"
    SUB_TITLE = "Navigate with ↑↓, expand with Enter, q to quit"

    CSS = """
    Screen {
        background: $surface;
    }
    Tree {
        background: $surface;
        scrollbar-gutter: stable;
        padding: 0 1;
    }
    Tree > .tree--cursor {
        background: $accent;
        color: $text;
    }
    #status-bar {
        height: 1;
        background: $panel;
        color: $text-muted;
        padding: 0 2;
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("e", "expand_all", "Expand all"),
        Binding("c", "collapse_all", "Collapse all"),
    ]

    def __init__(self, root_path: str, walker: TreeWalker):
        super().__init__()
        self.root_path = root_path
        self.walker = walker
        self._nodes: List[TreeNode] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Tree(self.root_path, id="filetree")
        yield Label("", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one("#filetree", Tree)
        root_name = Path(self.root_path).resolve().name or "."
        tree.root.label = f"{get_icon(root_name, is_dir=True)} {root_name}"

        self._nodes = self.walker.walk()
        self._populate_tree(tree.root, self._nodes)
        tree.root.expand()

        dirs = self.walker.total_dirs
        files = self.walker.total_files
        self.query_one("#status-bar", Label).update(
            f"  {dirs} director{'y' if dirs == 1 else 'ies'}, {files} file{'s' if files != 1 else ''}  |  Press 'q' to quit"
        )

    def _populate_tree(self, parent: TextualTreeNode, nodes: List[TreeNode]):
        for node in nodes:
            icon = get_icon(node.entry.name, is_dir=node.entry.is_dir, is_symlink=node.entry.is_symlink)
            label = f"{icon} {node.entry.name}"

            if node.entry.is_dir:
                child_node = parent.add(label, expand=False)
                if node.children:
                    self._populate_tree(child_node, node.children)
            else:
                parent.add_leaf(label)

    def action_expand_all(self) -> None:
        tree = self.query_one("#filetree", Tree)
        self._expand_all(tree.root)

    def _expand_all(self, node: TextualTreeNode) -> None:
        node.expand()
        for child in node.children:
            self._expand_all(child)

    def action_collapse_all(self) -> None:
        tree = self.query_one("#filetree", Tree)
        for child in tree.root.children:
            child.collapse_all()


def run_tui(root_path: str, walker: TreeWalker):
    app = FileTreeApp(root_path, walker)
    app.run()
