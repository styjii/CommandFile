from pathlib import Path
import shutil
from typing import List, Union, Optional
import typer


class OutputLogger:
    """Stores and retrieves styled terminal output."""
    def __init__(self) -> None:
        self._log_entries: List[str] = []

    def _log(self, content: str) -> None:
        self._log_entries.append(content)

    @property
    def styled_output(self) -> str:
        """Return all styled log entries."""
        return "\n".join(self._log_entries)


class Styler(OutputLogger):
    """Handles styling of terminal text."""
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return "Styler()"

    def apply_style(self, text: Union[List[str], str], save: Optional[bool] = True, **kwargs) -> Optional[str]:
        if isinstance(text, list):
            styled = "".join([typer.style(text=t, **kwargs) for t in text])
        else:
            styled = typer.style(text=text, **kwargs)

        if not save:
            return styled
        self._log(styled)
        return None

    def directory(self, name: str, save: Optional[bool] = False) -> Optional[str]:
        return self.apply_style(name, fg=typer.colors.BRIGHT_MAGENTA, bold=True, reset=False, save=save)

    def filename(self, name: str, save: Optional[bool] = False) -> Optional[str]:
        return self.apply_style(name, fg=typer.colors.YELLOW, bold=True, reset=False, save=save)

    def success(self, message: Union[List[str], str], save: Optional[bool] = True) -> Optional[str]:
        return self.apply_style(message, fg=typer.colors.BRIGHT_GREEN, save=save)

    def error(self, message: Union[List[str], str], save: Optional[bool] = True) -> Optional[str]:
        return self.apply_style(message, fg=typer.colors.BRIGHT_RED, save=save)

    def info(self, message: Union[List[str], str], save: Optional[bool] = True) -> Optional[str]:
        return self.apply_style(message, fg=typer.colors.BRIGHT_WHITE, italic=True, save=save)

    def heading(self, title: Union[List[str], str], save: Optional[bool] = True) -> Optional[str]:
        return self.apply_style(title, fg=typer.colors.BRIGHT_WHITE, bg=typer.colors.BLUE, save=save)

    def s_extension(self, text: Union[List[str], str], save: Optional[bool] = True) -> Optional[str]:
        return self.apply_style(text, bold=True, italic=True, save=save)


class FileManager(Styler):
    """Manages file operations such as search, copy, move, and delete."""
    def __init__(
        self,
        extension: str,
        source: Union[str, Path],
        destination: Optional[Union[str, Path]] = None,
        filename_prefix: Optional[str] = None
    ) -> None:
        super().__init__()
        self.extension = extension
        self.source_dir = Path(source)
        self.destination_dir = Path(destination) if destination else None
        self.filename_prefix = filename_prefix

    def __repr__(self) -> str:
        return f"FileManager({self.source_dir}, {self.destination_dir})"

    def _match_files(self, directory: Path, recursive: bool = True) -> List[Path]:
        prefix = f"*{self.filename_prefix}" if self.filename_prefix else ""
        pattern = f"{prefix}*.{self.extension}"
        return list(directory.rglob(pattern) if recursive else directory.glob(pattern))

    def _check_dirs(self) -> bool:
        if not self.source_dir.exists():
            self.error(["Source directory ", self.directory(str(self.source_dir)), " does not exist."])
            return False
        if self.destination_dir and not self.destination_dir.exists():
            self.error(["Destination directory ", self.directory(str(self.destination_dir)), " does not exist."])
            return False
        return True

    def _handle_files(self, action: str) -> None:
        if not self._check_dirs():
            return

        self.heading(f"{action.upper()} FILES:")
        source_files = self._match_files(self.source_dir)

        success_count = failed_count = 0

        for file in source_files:
            destination_filenames = [f.name for f in self._match_files(self.destination_dir, recursive=False)]
            name = file.name
            styled_name = self.filename(name)

            if name not in destination_filenames:
                try:
                    if action == "copy":
                        shutil.copy(file, self.destination_dir)
                    elif action == "move":
                        shutil.move(file, self.destination_dir)
                    self.success([f"{action.title().replace('y', 'ie')}d file ", styled_name])
                    success_count += 1
                except Exception as e:
                    self.error([f"Failed to {action} file {styled_name}: {e}"])
                    failed_count += 1
            else:
                self.error(["File ", styled_name, " already exists in destination."])
                failed_count += 1

        self.info([
            self.success(str(success_count), save=False), f" {action.replace('y', 'ie')}d, ",
            self.error(str(failed_count), save=False), " skipped."
        ])

    def find(self) -> None:
        if not self._check_dirs():
            return

        self.heading("FILES LIST:")
        files = self._match_files(self.source_dir)
        for file in files:
            self.success(["File ", self.filename(file.name), " in ", self.directory(str(file.parent))])

        self.info([
            f"Found {len(files)} ",
            self.s_extension(f"'.{self.extension}'", save=False),
            " files in ",
            self.directory(str(self.source_dir))
        ])

    def copy(self) -> None:
        self._handle_files("copy")

    def move(self) -> None:
        self._handle_files("move")

    def delete(self) -> None:
        if not self._check_dirs():
            return

        self.heading("DELETE FILES:")
        files = self._match_files(self.source_dir)
        deleted = 0

        for file in files:
            self.filename(file.name)
            file.unlink()
            self.success(["Deleted file ", self.filename(file.name)])
            deleted += 1

        self.info([
            self.success(str(deleted), save=False),
            " files deleted in ",
            self.directory(str(self.source_dir))
        ])


if __name__ == "__main__":
    def main() -> None:
        base_path = Path("/sdcard")
        manager = FileManager("txt", base_path, filename_prefix="algorithme")
        manager.find()
        typer.echo(manager.styled_output)

    typer.run(main)
