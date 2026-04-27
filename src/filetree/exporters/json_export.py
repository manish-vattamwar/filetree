"""
JSON exporter.
"""
import json
from typing import List
from filetree.walker import TreeNode

def export_json(nodes: List[TreeNode], root_path: str) -> str:
    def node_to_dict(node: TreeNode):
        data = {
            "name": node.entry.name,
            "type": "directory" if node.entry.is_dir else ("symlink" if node.entry.is_symlink else "file"),
            "size": node.entry.size,
            "mtime": node.entry.mtime,
            "mode": node.entry.mode
        }
        if node.entry.is_dir:
            data["children"] = [node_to_dict(c) for c in node.children]
        return data
        
    result = {
        "root": root_path,
        "tree": [node_to_dict(n) for n in nodes]
    }
    return json.dumps(result, indent=2)
