"""Data models for CLI argument parsing."""

from dataclasses import dataclass


@dataclass
class ParsedArguments:
    """Represents parsed command-line arguments.
    
    Attributes:
        query: The natural language query string
        file_path: Optional path to a file to attach to the query
        model: The AI model to use for the query
        provider: The AI provider name (e.g., 'perplexity')
        show_sources: Whether to display source citations
        flags: Additional boolean flags passed by the user
    """
    query: str
    file_path: str | None
    model: str
    provider: str
    show_sources: bool
    flags: dict[str, bool]
