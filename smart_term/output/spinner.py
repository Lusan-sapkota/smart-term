"""Thinking spinner for displaying loading animation during API calls."""

from rich.spinner import Spinner
from rich.live import Live


class ThinkingSpinner:
    """Context manager for displaying a thinking animation during API calls."""
    
    def __init__(self, message: str = "Thinking..."):
        """
        Initialize the thinking spinner.
        
        Args:
            message: The message to display alongside the spinner animation
        """
        self.message = message
        self.spinner = Spinner("dots", text=message)
        self.live = None
    
    def __enter__(self):
        """Start the spinner animation when entering the context."""
        self.live = Live(self.spinner, refresh_per_second=10)
        self.live.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the spinner animation when exiting the context."""
        if self.live:
            self.live.stop()
        return False  # Don't suppress exceptions
