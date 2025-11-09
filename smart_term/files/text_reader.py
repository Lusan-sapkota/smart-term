"""
Text file reader for plain text files.

This module handles reading and processing of plain text files
with UTF-8 encoding.
"""

import os
from smart_term.files.models import FileContent


class TextReader:
    """
    Reader for plain text files.
    
    Handles reading text files with UTF-8 encoding and returns
    structured FileContent objects.
    """
    
    def read(self, file_path: str) -> FileContent:
        """
        Read a text file and return its content.
        
        Args:
            file_path: Path to the text file to read
            
        Returns:
            FileContent object with type='text' and the file content
            
        Raises:
            FileNotFoundError: If the file does not exist
            UnicodeDecodeError: If the file cannot be decoded as UTF-8
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_size = os.path.getsize(file_path)
        
        return FileContent(
            type='text',
            content=content,
            metadata={
                'encoding': 'utf-8',
                'size_bytes': file_size
            },
            file_path=file_path
        )
