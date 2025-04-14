from typing import List, Union, Tuple, Optional
import typer


class CustomTyperStyle:
    """Custom terminal styling for commands using Typer."""
    
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


class LoadData(CustomTyperStyle):
    """Manages styled output history."""
    def __init__(self):
        self.data_typer_contents: List[str] = []

    def _add_content(self, content: str):
        """Store a styled string in the output log."""
        self.data_typer_contents.append(content)

    def load_file(self) -> str:
        """Return all styled log entries."""
        return "\n".join(self.data_typer_contents)


if __name__ == '__main__':
    def main():
        # test project
        cmd = LoadData()
        
        
        # (File script.py::fg=YELLOW,bold=True in /sdcard/test::BRIGHT_MAGENTA,bold)::fg=BRIGHT_GREEN
        cmd.success_style(["File ", cmd.file_style("script.py"), " in ", cmd.directory_style("/sdcard/test")])
        
        # (moved file script.py::fg=YELLOW,bold=True)::fg=BRIGHT_GREEN
        cmd.success_style(["moved file ", cmd.file_style("script.py")])
        
        # Save the text styled in a list and view
        for data_typer_content in cmd.data_typer_contents:
            typer.echo(data_typer_content)
    typer.run(main)