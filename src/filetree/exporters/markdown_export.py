"""
Markdown exporter.
"""
from typing import List
from filetree.walker import TreeNode
from filetree.icons import get_icon

def export_markdown(nodes: List[TreeNode], root_path: str, show_icons: bool = True) -> str:
    lines = []
    
    root_icon = get_icon(root_path, is_dir=True) if show_icons else ""
    lines.append(f"# {root_icon} {root_path}".strip())
    lines.append("")
    
    def walk(nodes_list: List[TreeNode], depth: int):
        indent = "  " * depth
        for node in nodes_list:
            icon_str = f"{get_icon(node.entry.name, node.entry.is_dir, node.entry.is_symlink)} " if show_icons else ""
            lines.append(f"{indent}- {icon_str}{node.entry.name}")
            if node.children:
                walk(node.children, depth + 1)
                
    walk(nodes, 0)
    return "\n".join(lines)
