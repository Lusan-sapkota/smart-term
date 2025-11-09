"""Output formatting for terminal display using Rich and Colorama."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from colorama import Fore, Style, init


class OutputFormatter:
    """Handles formatted output to the terminal with Rich and Colorama."""
    
    def __init__(self):
        """Initialize the output formatter with Rich Console and Colorama."""
        self.console = Console()
        init(autoreset=True)  # Initialize Colorama with auto-reset
    
    def display_query(self, query: str, file_info: dict | None = None):
        """
        Display the user's query with formatting.
        
        Args:
            query: The user's natural language query
            file_info: Optional dictionary with file information (path, type, size)
        """
        # Display query header
        self.console.print("\n[bold cyan]Query:[/bold cyan]")
        self.console.print(f"  {query}")
        
        # Display file attachment info if present
        if file_info:
            file_path = file_info.get('file_path', 'Unknown')
            file_type = file_info.get('type', 'unknown')
            self.console.print(f"\n[dim]📎 Attached file: {file_path} (type: {file_type})[/dim]")
        
        self.console.print()  # Add spacing
    
    def display_response(self, response: str, model: str):
        """
        Render the AI response with markdown formatting in a Rich Panel.
        
        Args:
            response: The AI model's response text (may include citations)
            model: The name of the model that generated the response
        """
        # Check if response contains citations
        if "__CITATIONS__" in response:
            main_response, citations_section = response.split("__CITATIONS__", 1)
            
            # Display main response
            md = Markdown(main_response.strip())
            panel = Panel(
                md,
                title=f"[bold green]Response from {model}[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(panel)
            
            # Display citations in a separate panel
            citations_panel = Panel(
                citations_section.strip(),
                title="[bold cyan]📚 Sources[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            )
            self.console.print(citations_panel)
            self.console.print()
        else:
            # No citations, display normally
            md = Markdown(response)
            panel = Panel(
                md,
                title=f"[bold green]Response from {model}[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(panel)
            self.console.print()  # Add spacing after response
    
    def display_error(self, error: Exception):
        """
        Display error messages with red styling.
        
        Args:
            error: The exception to display
        """
        error_message = str(error)
        error_type = type(error).__name__
        
        # Create error panel with red styling
        panel = Panel(
            f"[bold red]{error_type}:[/bold red]\n{error_message}",
            title="[bold red]Error[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def display_info(self, message: str):
        """
        Display informational messages with neutral styling.
        
        Args:
            message: The informational message to display
        """
        self.console.print(f"[bold blue]ℹ[/bold blue]  {message}")
