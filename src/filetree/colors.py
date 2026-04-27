"""
Color definitions using rich.
"""

from rich.style import Style
from rich.theme import Theme

# Core styles
DIR_STYLE = Style(color="blue", bold=True)
FILE_STYLE = Style(color="default")
SYMLINK_STYLE = Style(color="cyan")
EXEC_STYLE = Style(color="green")
TREE_LINE_STYLE = Style(color="bright_black")

# Predefined theme for easy usage
filetree_theme = Theme({
    "tree.dir": DIR_STYLE,
    "tree.file": FILE_STYLE,
    "tree.symlink": SYMLINK_STYLE,
    "tree.exec": EXEC_STYLE,
    "tree.line": TREE_LINE_STYLE,
})
