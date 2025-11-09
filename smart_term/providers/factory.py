"""
Provider factory for creating AI provider instances.

This module implements the factory pattern for instantiating AI provider
implementations based on configuration, enabling easy extensibility.
"""

import os
from typing import Optional

from .base import AIProvider
from .perplexity import PerplexityProvider
from ..utils.errors import MissingAPIKeyError, UnsupportedProviderError


class ProviderFactory:
    """
    Factory class for creating AI provider instances.
    
    This factory handles provider instantiation, credential management,
    and provides a clean interface for adding new providers in the future.
    """
    
    @staticmethod
    def create_provider(
        provider_name: str, 
        config: Optional[dict] = None
    ) -> AIProvider:
        """
        Create and return an AI provider instance.
        
        Args:
            provider_name: Name of the provider ('perplexity', 'gemini', etc.)
            config: Optional configuration dictionary for provider-specific settings
        
        Returns:
            An instance of AIProvider implementation
            
        Raises:
            MissingAPIKeyError: If required API key is not found
            UnsupportedProviderError: If provider is not supported
        """
        config = config or {}
        
        if provider_name == "perplexity":
            return ProviderFactory._create_perplexity_provider(config)
        
        # Future provider implementations:
        # elif provider_name == "gemini":
        #     return ProviderFactory._create_gemini_provider(config)
        # elif provider_name == "local":
        #     return ProviderFactory._create_local_provider(config)
        
        else:
            raise UnsupportedProviderError(
                f"Provider '{provider_name}' is not supported. "
                f"Available providers: perplexity"
            )
    
    @staticmethod
    def _create_perplexity_provider(config: dict) -> PerplexityProvider:
        """
        Create a Perplexity provider instance.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            PerplexityProvider instance
            
        Raises:
            MissingAPIKeyError: If PERPLEXITY_API_KEY is not set
        """
        api_key = os.getenv("PERPLEXITY_API_KEY")
        
        if not api_key:
            raise MissingAPIKeyError(
                "PERPLEXITY_API_KEY environment variable is not set.\n\n"
                "To set up your API key:\n"
                "1. Get your API key from https://www.perplexity.ai/settings/api\n"
                "2. Set the environment variable:\n"
                "   export PERPLEXITY_API_KEY='your-api-key-here'\n"
                "3. Or add it to your ~/.bashrc or ~/.zshrc for persistence"
            )
        
        # Get base URL from config if provided, otherwise use default
        base_url = config.get("perplexity_base_url", "https://api.perplexity.ai")
        
        return PerplexityProvider(api_key=api_key, base_url=base_url)
    
    # Future provider factory methods can be added here:
    # 
    # @staticmethod
    # def _create_gemini_provider(config: dict) -> GeminiProvider:
    #     """Create a Gemini provider instance."""
    #     api_key = os.getenv("GEMINI_API_KEY")
    #     if not api_key:
    #         raise MissingAPIKeyError("GEMINI_API_KEY environment variable is not set")
    #     return GeminiProvider(api_key=api_key)
    #
    # @staticmethod
    # def _create_local_provider(config: dict) -> LocalProvider:
    #     """Create a local model provider instance."""
    #     model_path = config.get("local_model_path")
    #     if not model_path:
    #         raise ConfigurationError("local_model_path not specified in configuration")
    #     return LocalProvider(model_path=model_path)
