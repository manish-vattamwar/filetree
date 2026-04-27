"""
HTML exporter.
"""
from typing import List
from filetree.walker import TreeNode
from filetree.icons import get_icon

def export_html(nodes: List[TreeNode], root_path: str, show_icons: bool = True) -> str:
    lines = []
    lines.append("<!DOCTYPE html>")
    lines.append("<html>")
    lines.append("<head>")
    lines.append("  <meta charset='utf-8'>")
    lines.append("  <title>FileTree Export</title>")
    lines.append("  <style>")
    lines.append("    body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }")
    lines.append("    details { margin-left: 20px; }")
    lines.append("    summary { cursor: pointer; user-select: none; color: #569cd6; }")
    lines.append("    summary:hover { color: #9cdcfe; }")
    lines.append("    .file { margin-left: 20px; color: #cccccc; padding: 2px 0; }")
    lines.append("  </style>")
    lines.append("</head>")
    lines.append("<body>")
    
    root_icon = get_icon(root_path, is_dir=True) if show_icons else ""
    lines.append(f"  <h2>{root_icon} {root_path}</h2>")
    
    def walk(nodes_list: List[TreeNode], indent_level: int):
        indent = "  " * indent_level
        for node in nodes_list:
            icon_str = f"{get_icon(node.entry.name, node.entry.is_dir, node.entry.is_symlink)} " if show_icons else ""
            if node.entry.is_dir:
                lines.append(f"{indent}<details open>")
                lines.append(f"{indent}  <summary>{icon_str}{node.entry.name}</summary>")
                walk(node.children, indent_level + 1)
                lines.append(f"{indent}</details>")
            else:
                lines.append(f"{indent}<div class='file'>{icon_str}{node.entry.name}</div>")
                
    walk(nodes, 1)
    
    lines.append("</body>")
    lines.append("</html>")
    
    return "\n".join(lines)
