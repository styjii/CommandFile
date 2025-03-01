from file_manager import FileManager

def test_search_files(tmp_path):
    test_file = tmp_path / "example.txt"
    test_file.write_text("Sample content")

    manager = FileManager(extension="txt", source=tmp_path)
    files_found = manager._match_files(directory=tmp_path)

    assert test_file in files_found
    assert len(files_found) == 1

def test_copy_files(tmp_path):
    src_dir = tmp_path / "source"
    dst_dir = tmp_path / "destination"
    src_dir.mkdir()
    dst_dir.mkdir()

    test_file = src_dir / "file.txt"
    test_file.write_text("Content")

    manager = FileManager("txt", source=src_dir, destination=dst_dir)
    manager.copy()

    copied_file = dst_dir / "file.txt"
    assert copied_file.exists()
    assert copied_file.read_text() == "Content"

def test_move_files(tmp_path):
    src_dir = tmp_path / "source"
    dst_dir = tmp_path / "destination"
    src_dir.mkdir()
    dst_dir.mkdir()

    test_file = src_dir / "file.txt"
    test_file.write_text("Content")

    manager = FileManager("txt", source=src_dir, destination=dst_dir)
    manager.move()

    moved_file = dst_dir / "file.txt"
    assert moved_file.exists()
    assert not test_file.exists()

def test_delete_files(tmp_path):
    src_dir = tmp_path / "source"
    src_dir.mkdir()

    test_file = src_dir / "file.txt"
    test_file.write_text("Content")

    manager = FileManager("txt", source=src_dir)
    manager.delete()

    assert not test_file.exists()