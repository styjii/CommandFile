from typing import List, Union, Tuple, Optional
import typer


class CustomTyperStyle:
    """Custom terminal styling for commands using Typer."""
    def __repr__(self) -> str: return "CustomTyperStyle()"

    def style(self, content: Union[List[str], str], **kwargs) -> Optional[str]:
        """
        Style text or a list of texts for terminal output.
        """
        if isinstance(content, list):
            content = "".join([
                typer.style(text=c, **kwargs) for c in content
            ])
        else:
            content = typer.style(text=content, **kwargs)

        return content

    def directory_style(self, directory: str):
        """Style for directory names."""
        return self.style(directory, fg=typer.colors.BRIGHT_MAGENTA, bold=True, reset=False)
    
    def file_style(self, file: str): 
        """Style for file names."""
        return self.style(file, fg=typer.colors.YELLOW, bold=True, reset=False)
    
    def success_style(self, content: Union[List[str], str]): 
        """Style for success messages."""
        return self.style(content, fg=typer.colors.BRIGHT_GREEN)
    
    def error_style(self, content: Union[List[str], str]): 
        """Style for error messages."""
        return self.style(content, fg=typer.colors.BRIGHT_RED)
    
    def info_style(self, content: Union[List[str], str]): 
        """Style for informational messages."""
        return self.style(content, fg=typer.colors.BRIGHT_WHITE, italic=True)
    
    def title_style(self, content: Union[List[str], str]): 
        """Style for section titles."""
        return self.style(content, fg=typer.colors.BRIGHT_WHITE, bg=typer.colors.BLUE)
    
    def extension_style(self, content: Union[List[str], str]): 
        """Style for extension names."""
        return self.style(content, bold=True, italic=True)


if __name__ == '__main__':
    def main():
        # test project
        cmd = CustomTyperStyle()
        
        
        # (File script.py::fg=YELLOW,bold=True in /sdcard/test::BRIGHT_MAGENTA,bold)::fg=BRIGHT_GREEN
        typer.echo(cmd.success_style(["File ", cmd.file_style("script.py"), " in ", cmd.directory_style("/sdcard/test")]))
    
    typer.run(main)