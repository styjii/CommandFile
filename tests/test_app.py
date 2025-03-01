from app import app
from typer.testing import CliRunner

cli_runner = CliRunner()

def test_search_command(tmp_path):
    file_path = tmp_path / "file.md"
    file_path.write_text("Markdown file")

    result = cli_runner.invoke(app, ["list-files", "md", str(tmp_path)])
    assert "file.md" in result.stdout
    assert result.exit_code == 0

def test_copy_command(tmp_path):
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    file_path = src_dir / "example.txt"
    file_path.write_text("Test content")

    result = cli_runner.invoke(app, ["copy-files", "txt", str(src_dir), str(dst_dir)])
    assert "Copied file" in result.stdout or "copied file" in result.stdout
    assert (dst_dir / "example.txt").exists()
    assert result.exit_code == 0

def test_move_command(tmp_path):
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    file_path = src_dir / "move.txt"
    file_path.write_text("Move this")

    result = cli_runner.invoke(app, ["move-files", "txt", str(src_dir), str(dst_dir)])
    assert "Moved file" in result.stdout or "moved file" in result.stdout
    assert (dst_dir / "move.txt").exists()
    assert not (src_dir / "move.txt").exists()
    assert result.exit_code == 0

def test_remove_command(tmp_path):
    file_path = tmp_path / "delete.txt"
    file_path.write_text("Delete this")

    result = cli_runner.invoke(app, ["remove-files", "txt", str(tmp_path)], input="y\n")
    assert "Deleted file" in result.stdout or "deleted file" in result.stdout
    assert not file_path.exists()
    assert result.exit_code == 0
