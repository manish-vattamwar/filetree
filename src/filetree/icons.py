"""
Icon registry for FileTree.
Maps file extensions and filenames to Unicode/Emoji icons.
"""

FOLDER_ICON = "📁"
FILE_ICON = "📄"
SYMLINK_ICON = "🔗"

EXTENSION_ICONS = {
    # Languages
    ".py":    "🐍",
    ".js":    "🟨",
    ".ts":    "🔷",
    ".rs":    "🦀",
    ".go":    "🐹",
    ".java":  "☕",
    ".rb":    "💎",
    ".c":     "🔵",
    ".cpp":   "🔵",
    ".h":     "📋",
    ".cs":    "🎯",
    ".php":   "🐘",
    ".swift": "🐦",
    ".kt":    "🇰",
    ".dart":  "🎯",

    # Web
    ".html":  "🌐",
    ".css":   "🎨",
    ".scss":  "🎨",
    ".sass":  "🎨",
    ".less":  "🎨",

    # Data & Config
    ".json":  "⚙️",
    ".yaml":  "⚙️",
    ".yml":   "⚙️",
    ".toml":  "⚙️",
    ".ini":   "⚙️",
    ".xml":   "📋",
    ".csv":   "📊",

    # Docs
    ".md":    "📝",
    ".txt":   "📄",
    ".pdf":   "📕",
    ".doc":   "📘",
    ".docx":  "📘",

    # Media
    ".png":   "🖼️",
    ".jpg":   "🖼️",
    ".jpeg":  "🖼️",
    ".gif":   "🖼️",
    ".svg":   "🖼️",
    ".mp4":   "🎬",
    ".mkv":   "🎬",
    ".mp3":   "🎵",
    ".wav":   "🎵",

    # DevOps
    ".sh":    "🐚",
    ".bash":  "🐚",
    ".zsh":   "🐚",
    ".env":   "🔒",

    # Archives
    ".zip":   "📦",
    ".tar":   "📦",
    ".gz":    "📦",
    ".rar":   "📦",
    ".7z":    "📦",
}

FILENAME_ICONS = {
    "Dockerfile":       "🐳",
    "docker-compose.yml": "🐳",
    "Makefile":         "🔨",
    ".gitignore":       "🙈",
    ".dockerignore":    "🙈",
    "LICENSE":          "📜",
    "README.md":        "📖",
    "package.json":     "📦",
    "package-lock.json":"🔒",
    "yarn.lock":        "🔒",
    "requirements.txt": "📋",
    "pyproject.toml":   "🐍",
    "Cargo.toml":       "🦀",
    "go.mod":           "🐹",
}

def get_icon(filename: str, is_dir: bool = False, is_symlink: bool = False) -> str:
    """Get the appropriate icon for a file or directory."""
    if is_symlink:
        return SYMLINK_ICON
    if is_dir:
        return FOLDER_ICON
    
    # Check exact filename
    if filename in FILENAME_ICONS:
        return FILENAME_ICONS[filename]
        
    # Check extension
    import os
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    if ext in EXTENSION_ICONS:
        return EXTENSION_ICONS[ext]
        
    return FILE_ICON
