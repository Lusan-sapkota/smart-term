"""
Image file handler for encoding images for API transmission.

This module handles reading, validating, and encoding image files
to base64 format for transmission to vision-capable AI models.
"""

import os
import base64
from PIL import Image
from smart_term.files.models import FileContent


class ImageHandler:
    """
    Handler for image files.
    
    Handles opening, validating, and encoding images to base64
    for API transmission to vision models.
    """
    
    def read(self, file_path: str) -> FileContent:
        """
        Read an image file and encode it to base64.
        
        Args:
            file_path: Path to the image file to read
            
        Returns:
            FileContent object with type='image' and base64 encoded data
            
        Raises:
            FileNotFoundError: If the file does not exist
            PIL.UnidentifiedImageError: If the file is not a valid image
        """
        # Open and validate the image
        with Image.open(file_path) as img:
            # Get image metadata
            image_format = img.format
            image_size = img.size
            image_mode = img.mode
        
        # Read the file and encode to base64
        with open(file_path, 'rb') as f:
            image_bytes = f.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        file_size = os.path.getsize(file_path)
        
        return FileContent(
            type='image',
            content=encoded_image,
            metadata={
                'format': image_format,
                'size_pixels': image_size,
                'mode': image_mode,
                'size_bytes': file_size
            },
            file_path=file_path
        )
