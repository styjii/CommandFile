from command_color import MainCommand

from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()

@app.command('run')
def main(
    command: str = typer.Argument(..., help="Possible commands: list, copy, move, search, remove."),
    extension: str = typer.Argument(..., help="The file extension to target."),
    src_dir: str = typer.Argument(..., help="Source folder to operate in."),
    dst_dir: Optional[str] = typer.Argument(None, help="Destination folder for copy or move operations.")
) -> None:
    """
    Perform file operations based on the given command.

    Args:
        command: One of 'search', 'copy', 'move', or 'remove'.
        extension: File extension to match (e.g., 'txt').
        src_dir: Source directory where files are located.
        dst_dir: Destination directory (used for 'copy' and 'move' only).
    """
    cmd = MainCommand(extension, src_dir, dst_dir)
    
    if command.lower() == "search":
        cmd.search()
    elif command.lower() == "copy":
        cmd.copy()
    elif command.lower() == "move":
        cmd.move()
    elif command.lower() == "remove":
        typer.confirm(
            typer.style("Do you really want to delete?", fg=typer.colors.BRIGHT_BLUE, italic=True),
            abort=True
        )
        cmd.remove()
    else:
        cmd.error_style("Invalid command!")
    
    typer.echo(cmd.load_file())


# Ensure the data directory exists
data_directory = Path(__file__).parent / "data"
if not data_directory.exists():
    data_directory.mkdir()
    gitignore_file = data_directory / ".gitignore"
    gitignore_content = "# Automatically created by app\n*"
    with open(gitignore_file, "w") as f:
        f.write(gitignore_content)

@app.command()
def sh(extension: str, directory: Optional[str] = typer.Argument(None, help="Directory to list files from.")):
    """
    List files with the given extension in the specified directory.

    If no directory is provided, the default 'data' directory is used.
    """
    if not directory:
        directory = data_directory
    main(command="search", extension=extension, src_dir=directory, dst_dir=None)

@app.command()
def cp(extension: str, src_dir: str, dst_dir: Optional[str] = typer.Argument(None)):
    """
    Copy files with the given extension from the source to the destination directory.
    """
    if not dst_dir:
        dst_dir = data_directory
    main(command="copy", extension=extension, src_dir=src_dir, dst_dir=dst_dir)

@app.command()
def mv(extension: str, src_dir: str, dst_dir: Optional[str] = typer.Argument(None)):
    """
    Move files with the given extension from the source to the destination directory.
    """
    if not dst_dir:
        dst_dir = data_directory
    main(command="move", extension=extension, src_dir=src_dir, dst_dir=dst_dir)

@app.command()
def rm(extension: str, directory: Optional[str] = typer.Argument(None, help="Directory to remove files from.")):
    """
    Delete files with the given extension in the specified directory.

    If no directory is provided, the default 'data' directory is used.
    """
    if not directory:
        directory = data_directory
    main(command="remove", extension=extension, src_dir=directory, dst_dir=None)

if __name__ == '__main__':
    app()
