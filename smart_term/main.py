#!/usr/bin/env python3
"""
Main entry point for Smart-term CLI tool.

This module orchestrates all components to process user queries,
handle file attachments, communicate with AI providers, and
display formatted responses.
"""

import sys
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from smart_term.config.loader import ConfigLoader
from smart_term.cli.parser import ArgumentParser
from smart_term.providers.factory import ProviderFactory
from smart_term.files.handler import FileHandler
from smart_term.files.models import FileContent
from smart_term.output.formatter import OutputFormatter
from smart_term.output.spinner import ThinkingSpinner
from smart_term.utils.errors import (
    SmartTermError,
    MissingAPIKeyError,
    UnsupportedFileTypeError,
    FileSizeExceededError,
    APIError,
    ConfigurationError,
    UnsupportedProviderError
)
from smart_term.utils.logger import logger


def execute_query(args: list[str]) -> int:
    """
    Execute a query with the AI provider.
    
    This function orchestrates the entire query execution flow:
    1. Load configuration
    2. Parse arguments
    3. Validate API key
    4. Handle file attachments
    5. Create provider
    6. Send query with spinner
    7. Display response
    8. Handle errors
    
    Args:
        args: Command-line arguments (excluding program name)
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    formatter = OutputFormatter()
    
    try:
        # Load configuration
        logger.info("Loading configuration")
        config_loader = ConfigLoader()
        config = config_loader.load_config()
        
        # Parse arguments
        logger.info(f"Parsing arguments: {args}")
        parser = ArgumentParser(
            default_model=config.get('default_model', 'sonar'),
            default_provider=config.get('default_provider', 'perplexity')
        )
        parsed_args = parser.parse(args)
        
        # Validate that we have a query
        if not parsed_args.query and not parsed_args.file_path:
            formatter.display_error(Exception(
                "No query provided. Usage: ai [file_path] <query> [--s|--p|--r|--deep]"
            ))
            return 1
        
        # Handle file attachment if present
        file_content: Optional[FileContent] = None
        file_info: Optional[dict] = None
        
        if parsed_args.file_path:
            logger.info(f"Processing file: {parsed_args.file_path}")
            file_handler = FileHandler(max_size_mb=config.get('max_file_size_mb', 10))
            
            try:
                file_content = file_handler.read_file(parsed_args.file_path)
                file_info = {
                    'file_path': parsed_args.file_path,
                    'type': file_content.type,
                    'size': len(file_content.content) if isinstance(file_content.content, str) else len(file_content.content)
                }
                logger.info(f"File processed successfully: {file_content.type}")
            except FileNotFoundError as e:
                logger.error(f"File not found: {e}")
                formatter.display_error(e)
                return 2
            except UnsupportedFileTypeError as e:
                logger.error(f"Unsupported file type: {e}")
                formatter.display_error(e)
                return 3
            except FileSizeExceededError as e:
                logger.error(f"File size exceeded: {e}")
                formatter.display_error(e)
                return 4
        
        # Display the query
        formatter.display_query(parsed_args.query, file_info)
        
        # Create provider
        logger.info(f"Creating provider: {parsed_args.provider}")
        try:
            provider = ProviderFactory.create_provider(
                parsed_args.provider,
                config
            )
        except MissingAPIKeyError as e:
            logger.error(f"Missing API key: {e}")
            formatter.display_error(e)
            return 1
        except UnsupportedProviderError as e:
            logger.error(f"Unsupported provider: {e}")
            formatter.display_error(e)
            return 1
        
        # Send query with thinking spinner
        logger.info(f"Sending query to {parsed_args.provider} with model {parsed_args.model}")
        
        show_spinner = config.get('show_thinking_animation', True)
        response = None
        
        # Convert FileContent to dict if present
        file_content_dict = None
        if file_content:
            file_content_dict = {
                'type': file_content.type,
                'content': file_content.content,
                'metadata': file_content.metadata,
                'file_path': file_content.file_path
            }
        
        try:
            if show_spinner:
                with ThinkingSpinner("Thinking..."):
                    response = provider.send_query(
                        query=parsed_args.query,
                        model=parsed_args.model,
                        file_content=file_content_dict
                    )
            else:
                response = provider.send_query(
                    query=parsed_args.query,
                    model=parsed_args.model,
                    file_content=file_content_dict
                )
            
            logger.info("Query completed successfully")
        
        except APIError as e:
            logger.error(f"API error: {e}")
            formatter.display_error(e)
            return 5
        
        # Display response
        if response:
            formatter.display_response(response, parsed_args.model)
        else:
            formatter.display_error(Exception("No response received from AI provider"))
            return 5
        
        return 0
    
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        formatter.display_error(e)
        return 6
    
    except SmartTermError as e:
        logger.error(f"Smart-term error: {e}")
        formatter.display_error(e)
        return 1
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        formatter.display_error(Exception(f"Unexpected error: {e}"))
        return 1


def main() -> int:
    """
    Main entry point for the Smart-term CLI tool.
    
    Parses command-line arguments and executes the query.
    Handles top-level exceptions and ensures proper exit codes.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Get arguments (excluding program name)
        args = sys.argv[1:]
        
        # Check if no arguments provided
        if not args:
            print("Smart-term AI CLI Tool")
            print("\nUsage: ai [file_path] <query> [--s|--p|--r|--deep]")
            print("\nModel flags:")
            print("  --s      Use sonar model (default)")
            print("  --p      Use sonar-pro model")
            print("  --r      Use sonar-reasoning-pro model")
            print("  --deep   Use sonar-deep-research model")
            print("\nExamples:")
            print("  ai 'What is the capital of France?'")
            print("  ai document.pdf 'Summarize this document' --p")
            print("  ai ~/code/script.py 'Explain this code' --r")
            print("  ai image.png 'What is in this image?'")
            return 1
        
        # Execute the query
        return execute_query(args)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130  # Standard exit code for SIGINT
    
    except Exception as e:
        logger.exception(f"Fatal error in main: {e}")
        print(f"\nFatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
