"""
Logging configuration for smart-term.

This module sets up logging with file rotation to ~/.smart_term/logs/smart_term.log
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str = "smart_term", log_level: str = "INFO") -> logging.Logger:
    """
    Configure and return a logger instance with file rotation.
    
    Args:
        name: Logger name (default: "smart_term")
        log_level: Logging level as string (default: "INFO")
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger already configured
    if logger.handlers:
        return logger
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create log directory
    log_dir = Path.home() / ".smart_term" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create log file path
    log_file = log_dir / "smart_term.log"
    
    # Create rotating file handler (5 files, 10MB each)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger


# Create default logger instance for use across modules
logger = setup_logger()
