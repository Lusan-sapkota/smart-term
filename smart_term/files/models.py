"""
Data models for file handling.

This module defines data structures used for representing file content
and metadata throughout the file handling system.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class FileContent:
    """
    Represents the content and metadata of a processed file.
    
    Attributes:
        type: The type of file ('text', 'pdf', 'image')
        content: The file content (text string or base64 encoded bytes)
        metadata: Additional information about the file (encoding, size, etc.)
        file_path: The original path to the file
    """
    type: str
    content: str | bytes
    metadata: dict[str, Any]
    file_path: str
