"""Command-line argument parsing for Smart-term CLI."""

import os
import sys
from pathlib import Path

from smart_term.cli.models import ParsedArguments


class ArgumentParser:
    """Parses command-line arguments for the Smart-term CLI tool.
    
    Handles file path detection, model flag extraction, and query building.
    """
    
    # Model flag mappings (case-insensitive)
    MODEL_FLAGS = {
        '--s': 'sonar',
        '--p': 'sonar-pro',
        '--r': 'sonar-reasoning-pro',
        '--deep': 'sonar-deep-research'
    }
    
    # Valid model names for validation
    VALID_MODELS = ['sonar', 'sonar-pro', 'sonar-reasoning-pro', 'sonar-deep-research']
    
    def __init__(self, default_model: str = 'sonar', default_provider: str = 'perplexity'):
        """Initialize the argument parser.
        
        Args:
            default_model: Default AI model to use if no flag is provided
            default_provider: Default AI provider to use
        """
        self.default_model = default_model
        self.default_provider = default_provider
    
    def parse(self, args: list[str]) -> ParsedArguments:
        """Parse command-line arguments into a ParsedArguments object.
        
        Args:
            args: List of command-line arguments (excluding program name)
        
        Returns:
            ParsedArguments object with parsed values
        """
        # Detect and extract file path if present
        file_path, remaining_args = self.detect_file_path(args)
        
        # Extract model flag
        model, remaining_args = self.extract_model_flag(remaining_args)
        
        # Extract --no-sources flag
        show_sources, remaining_args = self.extract_sources_flag(remaining_args)
        
        # Build query from remaining arguments
        query = self.build_query(remaining_args)
        
        return ParsedArguments(
            query=query,
            file_path=file_path,
            model=model if model else self.default_model,
            provider=self.default_provider,
            show_sources=show_sources,
            flags={}
        )
    
    def detect_file_path(self, args: list[str]) -> tuple[str | None, list[str]]:
        """Detect if the first argument is a file path.
        
        Checks if the first argument exists as a file on the filesystem.
        Handles tilde expansion for home directory paths.
        
        Args:
            args: List of command-line arguments
        
        Returns:
            Tuple of (file_path or None, remaining_args)
        """
        if not args:
            return None, args
        
        # Check if first argument could be a file path
        potential_path = args[0]
        
        # Expand tilde to home directory
        expanded_path = os.path.expanduser(potential_path)
        
        # Check if the path exists as a file
        if os.path.isfile(expanded_path):
            return expanded_path, args[1:]
        
        return None, args
    
    def extract_model_flag(self, args: list[str]) -> tuple[str | None, list[str]]:
        """Extract model flag from arguments.
        
        Looks for model flags (--s, --p, --r, --deep) in the arguments.
        Case-insensitive matching for common typos (--S, --P, etc.)
        If multiple flags are found, uses the last one and displays a warning.
        Invalid flags are warned about and ignored.
        
        Args:
            args: List of command-line arguments
        
        Returns:
            Tuple of (model_name or None, remaining_args without model flags)
        """
        model = None
        remaining_args = []
        found_flags = []
        
        for arg in args:
            # Case-insensitive matching for model flags
            arg_lower = arg.lower()
            
            if arg_lower in self.MODEL_FLAGS:
                model = self.MODEL_FLAGS[arg_lower]
                found_flags.append(arg_lower)
            # Check if it looks like a model flag but is invalid
            elif arg.startswith('--') and arg[2:3].isalpha() and len(arg) <= 7:
                # Might be a typo or invalid model flag
                if arg_lower not in self.MODEL_FLAGS and arg_lower not in ['--show-sources', '--show-source', '--show-s']:
                    print(f"⚠ Warning: Unknown flag '{arg}'. Using default model.", file=sys.stderr)
                    print(f"   Valid model flags: --s, --p, --r, --deep", file=sys.stderr)
                remaining_args.append(arg)
            else:
                remaining_args.append(arg)
        
        # Warn if multiple model flags were provided
        if len(found_flags) > 1:
            print(f"⚠ Warning: Multiple model flags provided ({', '.join(found_flags)}). "
                  f"Using the last one: {found_flags[-1]}", file=sys.stderr)
        
        return model, remaining_args
    
    def extract_sources_flag(self, args: list[str]) -> tuple[bool, list[str]]:
        """Extract --show-sources flag from arguments.
        
        Supports multiple variations: --show-sources, --show-source, --show-s
        
        Args:
            args: List of command-line arguments
        
        Returns:
            Tuple of (show_sources boolean, remaining_args without flag)
        """
        show_sources = False  # Default: hide sources
        remaining_args = []
        
        # Accepted variations for showing sources
        source_flags = ['--show-sources', '--show-source', '--show-s']
        
        for arg in args:
            if arg.lower() in source_flags:
                show_sources = True
            else:
                remaining_args.append(arg)
        
        return show_sources, remaining_args
    
    def build_query(self, args: list[str]) -> str:
        """Build query string from remaining arguments.
        
        Concatenates all non-flag arguments into a single query string.
        
        Args:
            args: List of remaining command-line arguments
        
        Returns:
            Query string with arguments joined by spaces
        """
        return ' '.join(args)
