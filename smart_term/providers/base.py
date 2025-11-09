"""
Abstract base class for AI provider implementations.

This module defines the interface that all AI provider implementations must follow,
enabling extensibility and consistent behavior across different AI services.
"""

from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    """
    Abstract base class for AI provider implementations.
    
    All AI provider implementations (Perplexity, Gemini, local models, etc.)
    must inherit from this class and implement its abstract methods.
    """
    
    @abstractmethod
    def send_query(
        self, 
        query: str, 
        model: str, 
        file_content: Optional[dict] = None
    ) -> str:
        """
        Send a query to the AI provider and return the response.
        
        Args:
            query: The natural language query from the user
            model: The specific model to use (e.g., 'sonar', 'sonar-pro')
            file_content: Optional dictionary containing file data with keys:
                - 'type': File type ('text', 'pdf', 'image')
                - 'content': File content (str or bytes)
                - 'metadata': Additional file metadata
                - 'file_path': Original file path
        
        Returns:
            The AI model's response as a string
            
        Raises:
            APIError: If the API request fails
            NetworkError: If there are network connectivity issues
        """
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate that the provider's API credentials are valid.
        
        This method should make a lightweight API call to verify that
        the credentials (API key, tokens, etc.) are properly configured
        and accepted by the provider.
        
        Returns:
            True if credentials are valid, False otherwise
            
        Raises:
            APIError: If the validation request fails for reasons other
                     than invalid credentials
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> list[str]:
        """
        Return a list of model identifiers supported by this provider.
        
        Returns:
            List of model names/identifiers that can be used with send_query()
            
        Example:
            ['sonar', 'sonar-pro', 'sonar-reasoning-pro', 'sonar-deep-research']
        """
        pass
