"""Output formatting for terminal display using Rich and Colorama."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from colorama import Fore, Style, init


class OutputFormatter:
    """Handles formatted output to the terminal with Rich and Colorama."""
    
    def __init__(self):
        """Initialize the output formatter with Rich Console and Colorama."""
        self.console = Console(
            soft_wrap=True,  # Enable soft wrapping for better text flow
            legacy_windows=False,  # Better Windows terminal support
            force_terminal=True,  # Force terminal mode
            force_interactive=False  # Disable interactive features that might cause issues
        )
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
    
    def display_response(self, response: str, model: str, show_sources: bool = False):
        """
        Render the AI response with markdown formatting in a Rich Panel.
        
        Args:
            response: The AI model's response text (may include citations)
            model: The name of the model that generated the response
            show_sources: Whether to display source citations (default: False)
        """
        # Model name color mapping for visual distinction
        model_colors = {
            'sonar': 'cyan',
            'sonar-pro': 'magenta',
            'sonar-reasoning-pro': 'yellow',
            'sonar-deep-research': 'blue'
        }
        model_color = model_colors.get(model, 'green')
        
        # Get terminal width for proper sizing
        terminal_width = self.console.width
        # Reserve space for panel borders and padding (4 chars on each side)
        content_width = max(40, terminal_width - 8)
        
        # Check if response contains citations
        if "__CITATIONS__" in response:
            # Check if we have both versions
            if "__WITH_CITATIONS__" in response:
                parts = response.split("__WITH_CITATIONS__")
                clean_part = parts[0]
                with_citations_part = parts[1] if len(parts) > 1 else clean_part
                
                if show_sources:
                    # Use version with citation numbers in text
                    main_response, citations_section = with_citations_part.split("__CITATIONS__", 1)
                else:
                    # Use clean version without citation numbers
                    main_response, citations_section = clean_part.split("__CITATIONS__", 1)
            else:
                main_response, citations_section = response.split("__CITATIONS__", 1)
            
            # Display main response with proper wrapping
            md = Markdown(
                main_response.strip(), 
                code_theme="monokai", 
                inline_code_theme="monokai",
                justify="left"
            )
            panel = Panel(
                md,
                title=f"[bold {model_color}]Response from {model}[/bold {model_color}]",
                border_style=model_color,
                padding=(1, 2),
                expand=True,  # Expand to fill width
                width=terminal_width  # Use full terminal width
            )
            self.console.print(panel)
            
            # Display citations only if show_sources is True
            if show_sources:
                # Make URLs clickable with truncated display
                clickable_citations = self._make_urls_clickable(citations_section.strip())
                
                citations_panel = Panel(
                    clickable_citations,
                    title="[bold cyan]📚 Sources[/bold cyan]",
                    border_style="cyan",
                    padding=(1, 2),
                    expand=True,
                    width=terminal_width
                )
                self.console.print(citations_panel)
            self.console.print()
        else:
            # No citations, display normally
            md = Markdown(
                response, 
                code_theme="monokai", 
                inline_code_theme="monokai",
                justify="left"
            )
            panel = Panel(
                md,
                title=f"[bold {model_color}]Response from {model}[/bold {model_color}]",
                border_style=model_color,
                padding=(1, 2),
                expand=True,
                width=terminal_width
            )
            self.console.print(panel)
            self.console.print()  # Add spacing after response
    
    def _make_urls_clickable(self, citations: str) -> Text:
        """
        Make URLs clickable in terminal with truncated display text.
        Uses Rich Text object for proper formatting and clickable links.
        
        Args:
            citations: Raw citations text with URLs
        
        Returns:
            Rich Text object with clickable, truncated URLs
        """
        import re
        from urllib.parse import urlparse
        
        lines = citations.split('\n')
        text = Text()
        
        for i, line in enumerate(lines):
            # Skip marker lines
            if line.startswith('__'):
                continue
                
            # Match pattern like "[1] https://..."
            match = re.match(r'(\[\d+\])\s+(https?://[^\s]+)', line)
            if match:
                number, url = match.groups()
                try:
                    parsed = urlparse(url)
                    # Get domain without www
                    domain = parsed.netloc.replace('www.', '')
                    # Get first part of path (if exists)
                    path_parts = [p for p in parsed.path.split('/') if p]
                    path = path_parts[0] if path_parts else ''
                    
                    # Create shortened display
                    if path:
                        short_url = f"{domain}/{path}"
                    else:
                        short_url = domain
                    
                    # Limit total length
                    if len(short_url) > 60:
                        short_url = short_url[:57] + "..."
                    
                    # Add citation number
                    text.append(f"{number} ", style="bold cyan")
                    # Add clickable link
                    text.append(short_url, style=f"link {url}")
                    
                except Exception:
                    # If parsing fails, use original
                    text.append(line)
            else:
                if line.strip():  # Only add non-empty lines
                    text.append(line)
            
            # Add newline except for last line
            if i < len(lines) - 1 and line.strip():
                text.append("\n")
        
        return text
    
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
