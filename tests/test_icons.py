from filetree.icons import get_icon, FOLDER_ICON, FILE_ICON, SYMLINK_ICON

def test_get_icon_folder():
    assert get_icon("anything", is_dir=True) == FOLDER_ICON

def test_get_icon_symlink():
    assert get_icon("anything", is_symlink=True) == SYMLINK_ICON

def test_get_icon_extension():
    assert get_icon("script.py") == "🐍"
    assert get_icon("data.json") == "⚙️"
    assert get_icon("image.png") == "🖼️"

def test_get_icon_filename():
    assert get_icon("Dockerfile") == "🐳"
    assert get_icon(".gitignore") == "🙈"
    assert get_icon("Makefile") == "🔨"

def test_get_icon_unknown():
    assert get_icon("unknown.xyz") == FILE_ICON
