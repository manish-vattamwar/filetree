"""
Utility functions for FileTree.
"""
import stat
from datetime import datetime

def format_size(size_bytes: int) -> str:
    """Format file size in a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            if unit == 'B':
                return f"{size_bytes}{unit}"
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}PB"

def format_time(timestamp: float) -> str:
    """Format a Unix timestamp into a readable date string."""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_permissions(mode: int) -> str:
    """Format file mode into Unix rwx string."""
    return stat.filemode(mode)
