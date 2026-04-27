from rich.console import Console
from filetree.renderer import TreeRenderer
from filetree.walker import TreeWalker

def test_renderer_basic(tmp_path):
    (tmp_path / "file.txt").write_text("hi")
    
    # We can capture rich console output
    console = Console(force_terminal=False, color_system=None)
    
    walker = TreeWalker(str(tmp_path))
    renderer = TreeRenderer(console)
    
    # We can't easily capture Console print to a string without custom file output,
    # but we can at least ensure it doesn't crash
    renderer.render(str(tmp_path), walker)
