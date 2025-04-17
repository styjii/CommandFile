from typing import List, Optional, Union
from pathlib import Path


def extract_numbers_from_filename(filename: str) -> List[str]:
    """Extracts numbers from a given filename.

    It attempts to extract two sets of numbers: one from the start, one from the end.

    Args:
        filename (str): The stem (name without extension) of a file.

    Returns:
        List[str]: A list of number strings found in the filename.
    """
    numeric_chars = [char if char.isdigit() else " " for char in filename]
    number_string = "".join(numeric_chars).strip()

    extracted_numbers = number_string.split()
    return [str(int(num)) for num in extracted_numbers if num]



def find_files_with_extensions(
    extensions: Union[List[str], str],
    directory: Path
) -> List[Path]:
    """Finds files in a directory with specified extension(s).

    Args:
        extensions (Union[List[str], str]): A single extension or a list of extensions (e.g., 'mp4' or ['mp4', 'avi']).
        directory (Path): The path to search for files.

    Returns:
        List[Path]: List of file paths matching the extension(s).
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if isinstance(extensions, str):
        extensions = [extensions]

    matched_files = []
    for ext in extensions:
        matched_files.extend(directory.glob(f"*.{ext}"))

    return matched_files


def rename_files(
    extensions: Union[List[str], str],
    source_directory: Union[str, Path],
    name_template: str = "File number {number}",
    dry_run: bool = True
) -> None:
    """Renames files in a directory using numbers extracted from filenames.

    Args:
        extensions (Union[List[str], str]): File extension(s) to look for.
        source_directory (Union[str, Path]): Directory containing the files to rename.
        name_template (str, optional): Template for renaming files. Supports {numbers[0]} and {number}. Defaults to "File number {number}".
        dry_run (bool, optional): If True, prints planned renames without applying them. Defaults to True.
    """
    source_path = Path(source_directory)

    try:
        files = find_files_with_extensions(extensions, source_path)
    except FileNotFoundError as e:
        print(e)
        return

    renamed_count = 0

    for file in files:
        numbers = extract_numbers_from_filename(file.stem)
        if not numbers:
            print(f"[INFO] The '{file.stem}' does not contain a number")
            continue

        try:
            # Support both '{number} and {numbers[0]}' else '{numbers[0]} and {numbers[1]' in template
            new_filename = name_template.format(numbers=numbers, number=numbers[0])
            new_file_path = file.parent / f"{new_filename}{file.suffix}"

            if dry_run:
                print(f"[DRY RUN] {file} -> {new_file_path}")
            else:
                file.rename(new_file_path)
                print(f"[RENAMED] {file.name} -> {new_filename}{file.suffix}")

            renamed_count += 1

        except Exception as e:
            print(f"[ERROR] Failed to rename {file.name}: {e}")

    print(f"[SUMMARY] {renamed_count} file(s) processed.")


if __name__ == "__main__":
    target_directory = "/sdcard/drama"

    rename_files(
        extensions=["mp4", "avi"],
        source_directory=target_directory,
        name_template="TWO HEART E{numbers[0]}",
        dry_run=True  # Change to False to actually rename files
    )
