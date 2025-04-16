from command_color import FileManager
from pathlib import Path
from typing import Optional
import typer

app = typer.Typer()

@app.command('run')
def main(
    operation: str = typer.Argument(..., help="Possible operations: list, copy, move, search, remove."),
    file_extension: str = typer.Argument(..., help="The file extension to target."),
    source_dir: str = typer.Argument(..., help="Source folder to operate in."),
    destination_dir: Optional[str] = typer.Argument(None, help="Destination folder for copy or move operations."),
    filename_prefix: Optional[str] = typer.Option(None, help="File name to target.")
) -> None:
    """
    Perform file operations based on the given command.

    Args:
        operation: One of 'search', 'copy', 'move', or 'remove'.
        file_extension: File extension to match (e.g., 'txt').
        source_dir: Source directory where files are located.
        destination_dir: Destination directory (used for 'copy' and 'move' only).
    """
    manager = FileManager(file_extension, source_dir, destination_dir, filename_prefix)
    
    if operation.lower() == "search":
        manager.find()
    elif operation.lower() == "copy":
        manager.copy()
    elif operation.lower() == "move":
        manager.move()
    elif operation.lower() == "remove":
        typer.confirm(
            typer.style("Do you really want to delete?", fg=typer.colors.BRIGHT_BLUE, italic=True),
            abort=True
        )
        manager.delete()
    else:
        manager.error("Invalid operation!")
    
    typer.echo(manager.styled_output)


# Ensure the data directory exists
data_directory = Path(__file__).parent / "data"
if not data_directory.exists():
    data_directory.mkdir()
    gitignore_file = data_directory / ".gitignore"
    gitignore_content = "# Automatically created by app\n*"
    with open(gitignore_file, "w") as f:
        f.write(gitignore_content)

@app.command()
def list_files(file_extension: str, directory: Optional[str] = typer.Argument(None, help="Directory to list files from."), filename_prefix: Optional[str] = typer.Option(None, help="File name to target.")):
    """
    List files with the given extension in the specified directory.

    If no directory is provided, the default 'data' directory is used.
    """
    if not directory:
        directory = data_directory
    main(operation="search", file_extension=file_extension, source_dir=directory, destination_dir=None, filename_prefix=filename_prefix)

@app.command()
def copy_files(file_extension: str, source_dir: str, destination_dir: Optional[str] = typer.Argument(None), filename_prefix: Optional[str] = typer.Option(None, help="File name to target.")):
    """
    Copy files with the given extension from the source to the destination directory.
    """
    if not destination_dir:
        destination_dir = data_directory
    main(operation="copy", file_extension=file_extension, source_dir=source_dir, destination_dir=destination_dir, filename_prefix=filename_prefix)

@app.command()
def move_files(file_extension: str, source_dir: str, destination_dir: Optional[str] = typer.Argument(None), filename_prefix: Optional[str] = typer.Option(None, help="File name to target.")):
    """
    Move files with the given extension from the source to the destination directory.
    """
    if not destination_dir:
        destination_dir = data_directory
    main(operation="move", file_extension=file_extension, source_dir=source_dir, destination_dir=destination_dir, filename_prefix=filename_prefix)

@app.command()
def remove_files(file_extension: str, directory: Optional[str] = typer.Argument(None, help="Directory to remove files from."), filename_prefix: Optional[str] = typer.Option(None, help="File name to target.")):
    """
    Delete files with the given extension in the specified directory.

    If no directory is provided, the default 'data' directory is used.
    """
    if not directory:
        directory = data_directory
    main(operation="remove", file_extension=file_extension, source_dir=directory, destination_dir=None, filename_prefix=filename_prefix)

if __name__ == '__main__':
    app()
