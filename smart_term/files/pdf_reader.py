"""
PDF file reader for extracting text from PDF documents.

This module handles reading and text extraction from PDF files
using PyPDF2 library.
"""

import os
from PyPDF2 import PdfReader
from smart_term.files.models import FileContent


class PDFReader:
    """
    Reader for PDF files.
    
    Handles extracting text content from PDF files, including
    multi-page documents.
    """
    
    def read(self, file_path: str) -> FileContent:
        """
        Read a PDF file and extract its text content.
        
        Args:
            file_path: Path to the PDF file to read
            
        Returns:
            FileContent object with type='pdf' and extracted text
            
        Raises:
            FileNotFoundError: If the file does not exist
            Exception: If PDF cannot be read or parsed
        """
        reader = PdfReader(file_path)
        
        # Extract text from all pages
        text_content = []
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        
        # Combine all pages with page separators
        combined_text = '\n\n--- Page Break ---\n\n'.join(text_content)
        
        file_size = os.path.getsize(file_path)
        
        return FileContent(
            type='pdf',
            content=combined_text,
            metadata={
                'page_count': len(reader.pages),
                'size_bytes': file_size
            },
            file_path=file_path
        )
