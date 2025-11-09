"""
File handler orchestrator for managing file reading operations.

This module provides the main FileHandler class that orchestrates
file type detection, size validation, and delegates to appropriate
readers based on file type.
"""

import os
from pathlib import Path
from smart_term.files.models import FileContent
from smart_term.files.text_reader import TextReader
from smart_term.files.pdf_reader import PDFReader
from smart_term.files.image_handler import ImageHandler
from smart_term.utils.errors import UnsupportedFileTypeError, FileSizeExceededError


class FileHandler:
    """
    Orchestrator for file reading operations.
    
    Detects file types, validates file sizes, and delegates to
    appropriate readers for processing different file formats.
    """
    
    # Supported file extensions mapped to file types
    SUPPORTED_EXTENSIONS = {
        # Text files
        '.txt': 'text',
        '.md': 'text',
        '.py': 'text',
        '.js': 'text',
        '.json': 'text',
        '.yaml': 'text',
        '.yml': 'text',
        '.sh': 'text',
        '.html': 'text',
        '.css': 'text',
        '.xml': 'text',
        '.csv': 'text',
        '.log': 'text',
        '.ini': 'text',
        '.cfg': 'text',
        '.conf': 'text',
        '.rs': 'text',
        '.go': 'text',
        '.java': 'text',
        '.cpp': 'text',
        '.c': 'text',
        '.h': 'text',
        '.ts': 'text',
        '.tsx': 'text',
        '.jsx': 'text',
        # PDF files
        '.pdf': 'pdf',
        # Image files
        '.png': 'image',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.gif': 'image',
        '.webp': 'image',
        '.bmp': 'image',
    }
    
    def __init__(self, max_size_mb: int = 10):
        """
        Initialize the FileHandler.
        
        Args:
            max_size_mb: Maximum allowed file size in megabytes
        """
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
        
        # Initialize readers
        self.readers = {
            'text': TextReader(),
            'pdf': PDFReader(),
            'image': ImageHandler()
        }
    
    def detect_file_type(self, file_path: str) -> str:
        """
        Detect the file type based on file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type string ('text', 'pdf', or 'image')
            
        Raises:
            UnsupportedFileTypeError: If file extension is not supported
        """
        # Get file extension (lowercase)
        extension = Path(file_path).suffix.lower()
        
        if extension not in self.SUPPORTED_EXTENSIONS:
            supported_list = ', '.join(sorted(set(self.SUPPORTED_EXTENSIONS.keys())))
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {extension}. "
                f"Supported types: {supported_list}"
            )
        
        return self.SUPPORTED_EXTENSIONS[extension]
    
    def validate_file_size(self, file_path: str) -> None:
        """
        Validate that the file size is within allowed limits.
        
        Args:
            file_path: Path to the file
            
        Raises:
            FileSizeExceededError: If file exceeds maximum size
            FileNotFoundError: If file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        
        if file_size > self.max_size_bytes:
            size_mb = file_size / (1024 * 1024)
            raise FileSizeExceededError(
                f"File size ({size_mb:.2f}MB) exceeds maximum allowed "
                f"size of {self.max_size_mb}MB"
            )

    def read_file(self, file_path: str) -> FileContent:
        """
        Read a file using the appropriate reader based on file type.
        
        This is the main entry point for file reading. It orchestrates
        file type detection, size validation, and delegates to the
        appropriate reader.
        
        Args:
            file_path: Path to the file to read (supports tilde expansion)
            
        Returns:
            FileContent object with the file's content and metadata
            
        Raises:
            FileNotFoundError: If the file does not exist
            UnsupportedFileTypeError: If the file type is not supported
            FileSizeExceededError: If the file exceeds size limits
        """
        # Expand tilde in path
        expanded_path = os.path.expanduser(file_path)
        
        # Validate file exists and size is acceptable
        self.validate_file_size(expanded_path)
        
        # Detect file type
        file_type = self.detect_file_type(expanded_path)
        
        # Get appropriate reader
        reader = self.readers[file_type]
        
        # Read and return file content
        return reader.read(expanded_path)
