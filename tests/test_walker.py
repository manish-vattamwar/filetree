from filetree.walker import TreeWalker

def test_walker_basic(tmp_path):
    (tmp_path / "file1.txt").write_text("hi")
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file2.txt").write_text("hi")
    
    walker = TreeWalker(str(tmp_path))
    nodes = walker.walk()
    
    assert walker.total_dirs == 1
    assert walker.total_files == 2
    
    assert len(nodes) == 2
    assert nodes[0].entry.name == "dir1"
    assert nodes[0].entry.is_dir
    assert len(nodes[0].children) == 1
    assert nodes[0].children[0].entry.name == "file2.txt"

    assert nodes[1].entry.name == "file1.txt"
    assert not nodes[1].entry.is_dir

def test_walker_gitignore(tmp_path):
    (tmp_path / "file.txt").write_text("hi")
    (tmp_path / "ignored.log").write_text("ignore")
    (tmp_path / ".gitignore").write_text("*.log\n")
    
    walker = TreeWalker(str(tmp_path))
    nodes = walker.walk()
    
    names = [n.entry.name for n in nodes]
    assert "file.txt" in names
    assert ".gitignore" not in names # Hidden files are ignored
    assert "ignored.log" not in names
