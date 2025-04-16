from pathlib import Path
import shutil
from typing import List, Union, Optional
import typer



class LoadData:
    """Manages styled output history."""
    def __init__(self): self.data_typer_contents: List[str] = []

    def _add_content(self, content: str): self.data_typer_contents.append(content)

    @property
    def load_file(self) -> str:
        """Return all styled log entries."""
        return "\n".join(self.data_typer_contents)
        
        
class CustomTyperStyle(LoadData):
    """Custom terminal styling for commands using Typer."""
    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str: return "CustomTyperStyle()"

    def style(self, content: Union[List[str], str], saved: Optional[bool] = True, **kwargs) -> Optional[str]:
        """
        Style text or a list of texts for terminal output.
        """
        if isinstance(content, list):
            content = "".join([
                typer.style(text=c, **kwargs) for c in content
            ])
        else:
            content = typer.style(text=content, **kwargs)

        if not saved:
            return content
        self._add_content(content)

    def directory_style(self, directory: str, saved: Optional[bool] = False):
        """Style for directory names."""
        return self.style(directory, fg=typer.colors.BRIGHT_MAGENTA, bold=True, reset=False, saved=saved)
    
    def file_style(self, file: str, saved: Optional[bool] = False): 
        """Style for file names."""
        return self.style(file, fg=typer.colors.YELLOW, bold=True, reset=False, saved=saved)
    
    def success_style(self, content: Union[List[str], str], saved: Optional[bool] = True): 
        """Style for success messages."""
        return self.style(content, fg=typer.colors.BRIGHT_GREEN, saved=saved)
    
    def error_style(self, content: Union[List[str], str], saved: Optional[bool] = True): 
        """Style for error messages."""
        return self.style(content, fg=typer.colors.BRIGHT_RED, saved=saved)
    
    def info_style(self, content: Union[List[str], str], saved: Optional[bool] = True): 
        """Style for informational messages."""
        return self.style(content, fg=typer.colors.BRIGHT_WHITE, italic=True, saved=saved)
    
    def title_style(self, content: Union[List[str], str], saved: Optional[bool] = True): 
        """Style for section titles."""
        return self.style(content, fg=typer.colors.BRIGHT_WHITE, bg=typer.colors.BLUE, saved=saved)
    
    def extension_style(self, content: Union[List[str], str], saved: Optional[bool] = True): 
        """Style for extension names."""
        return self.style(content, bold=True, italic=True, saved=saved)


class MainCommand(CustomTyperStyle):
    """
    Handles file operations such as search, copy, move, and remove.

    Args:
        extension: File extension to target.
        from_dir: Source directory.
        to_dir: Destination directory.
    """
    def __init__(self, extension: str, from_dir: Union[str, Path], to_dir: Optional[Union[str, Path]] = None, filename: Optional[str] = None):
        super().__init__()
        self.extension = extension
        self.from_dir = Path(from_dir)
        self.to_dir = Path(to_dir) if to_dir else None
        self.filename = filename

    def __repr__(self): return f"Command({self.from_dir}, {self.to_dir})"

    def _find_files(self, directory: Path, recursive=True) -> List[Path]:
        filename = f"*{self.filename}" if self.filename else ""
        return list(directory.rglob(f"{filename}*.{self.extension}") if recursive else directory.glob(f"{filename}*.{self.extension}"))

    def _directories_exist(self) -> bool:
        if not self.from_dir.exists():
            self.error_style(["Source directory ", self.directory_style(str(self.from_dir)), " does not exist."])
            return False
        if self.to_dir and not self.to_dir.exists():
            self.error_style(["Destination directory ", self.directory_style(str(self.to_dir)), " does not exist."])
            return False
        return True
    
    def _process_files(self, action: str):
        if not self._directories_exist(): 
            return
        self.title_style(f"{action.upper()} FILES:")

        src_files = self._find_files(self.from_dir)

        success = failed = 0
        for src_file in src_files:
            filename = src_file.name
            file_styled = self.file_style(src_file)
            dst_files = [f.name for f in self._find_files(self.to_dir, recursive=False)] if self.to_dir else []
            if filename not in dst_files:
                try:
                    if action == "copy":
                        shutil.copy(src_file, self.to_dir)
                    elif action == "move":
                        shutil.move(src_file, self.to_dir)
                    self.success_style([f"{action.title().replace('y', 'ie')}d file ", file_styled])
                    success += 1
                except Exception as e:
                    self.error_style([f"Failed to {action} file {file_styled}: {e}"])
                    failed += 1
            else:
                self.error_style(["File ", file_styled, " already exists in destination."])
                failed += 1

        self.info_style([
            self.success_style(str(success), saved=False), f" {action.replace('y', 'ie')}d, ",
            self.error_style(str(failed), saved=False), " skipped."
        ])

    def search(self):
        """Search files with the given extension in the source directory."""
        if not self._directories_exist(): 
            return
        self.title_style("FILES LIST:")
        files = self._find_files(self.from_dir)
        for file in files:
            self.success_style(["File ", self.file_style(file.name), " in ", self.directory_style(str(file.parent))])
        self.info_style([f"Found {len(files)} " , self.extension_style(f"'.{self.extension}'", saved=False), " files in ", self.directory_style(str(self.from_dir))])

    def copy(self): 
        """Copy files to the destination directory."""
        self._process_files("copy")
    
    def move(self): 
        """Move files to the destination directory."""
        self._process_files("move")

    def remove(self):
        """Delete files with the given extension from the source directory."""
        if not self._directories_exist(): 
            return
        
        self.title_style("DELETE FILES:")
        files = self._find_files(self.from_dir)
        success = 0
        for file in files:
            self.file_style(file.name)
            file.unlink()
            self.success_style(["Deleted file ", self.file_style(file.name)])
            success += 1

        self.info_style([
            self.success_style(str(success), saved=False),
            " files deleted in ",
            self.directory_style(str(self.from_dir))
        ])


if __name__ == '__main__':
    def main():
        # base_dir = Path(__file__).parent / "data"
        base_dir = Path("E:\\")
        
        cmd = MainCommand("txt", base_dir, filename="algorithme")
        cmd.search()

        typer.echo(cmd.load_file)

    typer.run(main)