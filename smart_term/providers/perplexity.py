"""
Perplexity AI provider implementation.

This module implements the AIProvider interface for Perplexity AI's API,
supporting various Sonar models for natural language queries.
"""

import requests
from typing import Optional

from .base import AIProvider
from ..utils.errors import APIError


class PerplexityProvider(AIProvider):
    """
    Perplexity AI provider implementation.
    
    Supports Perplexity's Sonar models including standard, pro, reasoning, and deep research variants.
    """
    
    # Available Perplexity models
    AVAILABLE_MODELS = [
        "sonar",
        "sonar-pro",
        "sonar-reasoning-pro",
        "sonar-deep-research"
    ]
    
    def __init__(self, api_key: str, base_url: str = "https://api.perplexity.ai"):
        """
        Initialize the Perplexity provider.
        
        Args:
            api_key: Perplexity API key
            base_url: Base URL for Perplexity API (default: https://api.perplexity.ai)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = 30
    
    def send_query(
        self, 
        query: str, 
        model: str, 
        file_content: Optional[dict] = None
    ) -> str:
        """
        Send a query to Perplexity API and return the response.
        
        Args:
            query: The natural language query
            model: Model identifier (e.g., 'sonar', 'sonar-pro')
            file_content: Optional file content dictionary
        
        Returns:
            The AI model's response text
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Build the message content
        messages = []
        
        # If file content is provided, include it in the message
        if file_content:
            file_type = file_content.get('type')
            content = file_content.get('content')
            file_path = file_content.get('file_path', 'attached file')
            
            if file_type == 'text':
                # For text files, prepend the content to the query
                full_query = f"File content from {file_path}:\n\n{content}\n\n{query}"
                messages.append({
                    "role": "user",
                    "content": full_query
                })
            elif file_type == 'image':
                # For images, use multi-part content (if supported by API)
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{content}"}}
                    ]
                })
            else:
                # For other types (PDF), include as text
                full_query = f"Content from {file_path}:\n\n{content}\n\n{query}"
                messages.append({
                    "role": "user",
                    "content": full_query
                })
        else:
            # Simple text query
            messages.append({
                "role": "user",
                "content": query
            })
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            # Check for HTTP errors
            if response.status_code == 401:
                raise APIError("Authentication failed. Please check your API key.")
            elif response.status_code == 429:
                raise APIError("Rate limit exceeded. Please wait and try again.")
            elif response.status_code >= 400:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg += f": {error_data['error']}"
                except:
                    error_msg += f": {response.text}"
                raise APIError(error_msg)
            
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Extract the response text from the API response
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                raise APIError("Unexpected API response format")
                
        except requests.exceptions.Timeout:
            raise APIError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.ConnectionError:
            raise APIError("Network error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """
        Validate the API key by making a test request.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Minimal test payload
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "user", "content": "test"}
            ]
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            # If we get 401, credentials are invalid
            if response.status_code == 401:
                return False
            
            # Any other response (including success) means credentials are valid
            return True
            
        except requests.exceptions.RequestException:
            # Network errors don't indicate invalid credentials
            raise APIError("Unable to validate credentials due to network error")
    
    def get_available_models(self) -> list[str]:
        """
        Return list of available Perplexity models.
        
        Returns:
            List of model identifiers
        """
        return self.AVAILABLE_MODELS.copy()
