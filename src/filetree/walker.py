"""
Directory walking engine.
"""

import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Dict
import pathspec
import fnmatch

@dataclass
class FileEntry:
    path: Path
    name: str
    is_dir: bool
    is_symlink: bool
    size: int = 0
    mtime: float = 0.0
    mode: int = 0
    git_status: str = ""

@dataclass
class TreeNode:
    entry: FileEntry
    children: List['TreeNode']

class TreeWalker:
    def __init__(
        self, 
        root: str, 
        all_files: bool = False, 
        max_depth: Optional[int] = None, 
        dirs_only: bool = False,
        excludes: Optional[List[str]] = None,
        includes: Optional[List[str]] = None,
        sort_by: str = "name",
        show_git: bool = False
    ):
        self.root = Path(root).resolve()
        self.all_files = all_files
        self.max_depth = max_depth
        self.dirs_only = dirs_only
        self.excludes = excludes or []
        self.includes = includes or []
        self.sort_by = sort_by
        self.show_git = show_git
        self.gitignore_spec = self._load_gitignore()
        self.git_status_map = self._get_git_status() if show_git else {}
        self.total_dirs = 0
        self.total_files = 0

    def _get_git_status(self) -> Dict[Path, str]:
        status_map = {}
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain", "-z"],
                cwd=str(self.root),
                capture_output=True,
                text=True,
                check=True
            )
            entries = result.stdout.split('\0')
            i = 0
            while i < len(entries):
                entry = entries[i]
                if not entry:
                    i += 1
                    continue
                status_code = entry[:2]
                file_path = entry[3:]
                
                full_path = (self.root / file_path).resolve()
                status_map[full_path] = status_code
                
                # Renames have two paths in -z format
                if status_code[0] == 'R' or status_code[0] == 'C':
                    i += 2
                else:
                    i += 1
        except Exception:
            pass
        return status_map

    def _load_gitignore(self) -> Optional[pathspec.PathSpec]:
        if self.all_files:
            return None
        gitignore_path = self.root / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                lines.append(".git")
                return pathspec.PathSpec.from_lines('gitignore', lines)
        return pathspec.PathSpec.from_lines('gitignore', [".git"])

    def _is_ignored(self, path: Path) -> bool:
        name = path.name
        
        for pattern in self.excludes:
            if fnmatch.fnmatch(name, pattern):
                return True
                
        if self.includes and not path.is_dir():
            matched = False
            for pattern in self.includes:
                if fnmatch.fnmatch(name, pattern):
                    matched = True
                    break
            if not matched:
                return True

        if self.all_files:
            return False
            
        if name.startswith('.') and name != '.':
            return True
            
        if self.gitignore_spec:
            try:
                rel_path = path.relative_to(self.root)
                path_str = str(rel_path)
                if path.is_dir():
                    path_str += '/'
                return self.gitignore_spec.match_file(path_str)
            except ValueError:
                pass
        return False

    def walk(self) -> List[TreeNode]:
        self.total_dirs = 0
        self.total_files = 0
        nodes = self._walk_dir(self.root, 0)
        
        if self.includes:
            nodes = self._prune_empty_dirs(nodes)
            
        return nodes
        
    def _prune_empty_dirs(self, nodes: List[TreeNode]) -> List[TreeNode]:
        pruned = []
        for node in nodes:
            if node.entry.is_dir:
                node.children = self._prune_empty_dirs(node.children)
                if node.children:
                    pruned.append(node)
                else:
                    self.total_dirs -= 1
            else:
                pruned.append(node)
        return pruned

    def _walk_dir(self, current_dir: Path, current_depth: int) -> List[TreeNode]:
        if self.max_depth is not None and current_depth >= self.max_depth:
            return []

        try:
            entries = list(current_dir.iterdir())
            
            nodes = []
            for entry in entries:
                if self._is_ignored(entry):
                    continue
                    
                is_dir = entry.is_dir()
                if self.dirs_only and not is_dir:
                    continue
                
                try:
                    stat_res = entry.lstat() if entry.is_symlink() else entry.stat()
                    size = stat_res.st_size
                    mtime = stat_res.st_mtime
                    mode = stat_res.st_mode
                except OSError:
                    size = 0
                    mtime = 0.0
                    mode = 0
                    
                git_status = self.git_status_map.get(entry.resolve(), "")

                file_entry = FileEntry(
                    path=entry,
                    name=entry.name,
                    is_dir=is_dir,
                    is_symlink=entry.is_symlink(),
                    size=size,
                    mtime=mtime,
                    mode=mode,
                    git_status=git_status
                )
                
                children = []
                if is_dir:
                    children = self._walk_dir(entry, current_depth + 1)
                    
                nodes.append(TreeNode(entry=file_entry, children=children))
                
            if self.sort_by == "size":
                nodes.sort(key=lambda n: (not n.entry.is_dir, -n.entry.size))
            elif self.sort_by == "date":
                nodes.sort(key=lambda n: (not n.entry.is_dir, -n.entry.mtime))
            else:
                nodes.sort(key=lambda n: (not n.entry.is_dir, n.entry.name.lower()))
                
            for n in nodes:
                if n.entry.is_dir:
                    self.total_dirs += 1
                else:
                    self.total_files += 1

            return nodes
        except PermissionError:
            return []
