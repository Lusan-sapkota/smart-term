"""
Custom exception classes for smart-term.

This module defines all custom exceptions used throughout the application
for clear and specific error handling.
"""


class SmartTermError(Exception):
    """Base exception for all smart-term errors."""
    pass


class MissingAPIKeyError(SmartTermError):
    """Raised when a required API key is not found in environment variables."""
    pass


class UnsupportedFileTypeError(SmartTermError):
    """Raised when a file type is not supported for processing."""
    pass


class FileSizeExceededError(SmartTermError):
    """Raised when a file exceeds the maximum allowed size."""
    pass


class APIError(SmartTermError):
    """Raised when an API request fails."""
    pass


class ConfigurationError(SmartTermError):
    """Raised when configuration is invalid or cannot be loaded."""
    pass


class UnsupportedProviderError(SmartTermError):
    """Raised when an unsupported AI provider is requested."""
    pass
