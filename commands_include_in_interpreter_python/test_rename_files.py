from pathlib import Path
from rename_files import rename_files, find_files_with_extensions

def test_rename_files(tmp_path: Path):
    extension = "mp4"
    test_directory = [
        tmp_path / "drama01 4movies in1.mp4",
        tmp_path / "drama01 4movies in2.mp4",
        tmp_path / "drama01 4movies in3.mp4",
        tmp_path / "drama01 4movies in4.mp4",
    ]

    for test_file in test_directory:
        test_file.touch()

    rename_files(extension, tmp_path, "drama test saison-{numbers[0]} episode-{numbers[2]}", False)
    # files_renamed = rename_files(extension, tmp_path, "drama test saison-{number[0]} episode-{number[1]}", False)

    files_found = find_files_with_extensions(extension, tmp_path)

    for index in range(1, len(files_found) + 1):
        print([file.name for file in files_found])
        assert f"drama test saison-1 episode-{index}.mp4" in [file.name for file in files_found]