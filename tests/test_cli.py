from click.testing import CliRunner
from filetree.cli import cli

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Display directory structure with icons" in result.output

def test_cli_run(tmp_path):
    (tmp_path / "test.txt").write_text("hello")
    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path)])
    assert result.exit_code == 0
    assert "test.txt" in result.output
    assert "1 file" in result.output
