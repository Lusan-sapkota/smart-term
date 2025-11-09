"""Configuration loader for Smart-term CLI tool."""

import json
import os
from pathlib import Path
from typing import Any

from .defaults import DEFAULT_CONFIG


class ConfigLoader:
    """Loads and validates configuration from user's config file."""
    
    def __init__(self, config_path: str = "~/.ai_cli_config.json"):
        """Initialize ConfigLoader with config file path.
        
        Args:
            config_path: Path to configuration file (supports tilde expansion)
        """
        self.config_path = Path(config_path).expanduser()
    
    def load_config(self) -> dict[str, Any]:
        """Load configuration from file and merge with defaults.
        
        Returns:
            Dictionary containing merged configuration values
        """
        if not self.config_path.exists():
            # Config file doesn't exist, return defaults
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            if not self.validate_config(user_config):
                print(f"Warning: Invalid configuration in {self.config_path}. Using defaults.")
                return DEFAULT_CONFIG.copy()
            
            return self.merge_with_defaults(user_config)
        
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.config_path}: {e}")
            print("Using default configuration.")
            return DEFAULT_CONFIG.copy()
        
        except Exception as e:
            print(f"Error loading configuration: {e}")
            print("Using default configuration.")
            return DEFAULT_CONFIG.copy()
    
    def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate configuration values.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            True if configuration is valid, False otherwise
        """
        if not isinstance(config, dict):
            return False
        
        # Validate timeout
        if "timeout" in config:
            if not isinstance(config["timeout"], (int, float)) or config["timeout"] <= 0:
                print(f"Warning: Invalid timeout value '{config['timeout']}'. Must be a positive number.")
                return False
        
        # Validate max_file_size_mb
        if "max_file_size_mb" in config:
            if not isinstance(config["max_file_size_mb"], (int, float)) or config["max_file_size_mb"] <= 0:
                print(f"Warning: Invalid max_file_size_mb value '{config['max_file_size_mb']}'. Must be a positive number.")
                return False
        
        # Validate show_thinking_animation
        if "show_thinking_animation" in config:
            if not isinstance(config["show_thinking_animation"], bool):
                print(f"Warning: Invalid show_thinking_animation value '{config['show_thinking_animation']}'. Must be a boolean.")
                return False
        
        # Validate log_level
        if "log_level" in config:
            valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if config["log_level"] not in valid_log_levels:
                print(f"Warning: Invalid log_level '{config['log_level']}'. Must be one of {valid_log_levels}.")
                return False
        
        # Validate output_format
        if "output_format" in config:
            valid_formats = ["markdown", "plain"]
            if config["output_format"] not in valid_formats:
                print(f"Warning: Invalid output_format '{config['output_format']}'. Must be one of {valid_formats}.")
                return False
        
        return True
    
    def merge_with_defaults(self, user_config: dict[str, Any]) -> dict[str, Any]:
        """Merge user configuration with default values.
        
        Args:
            user_config: User's configuration dictionary
            
        Returns:
            Merged configuration with defaults for missing values
        """
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(user_config)
        return merged_config
