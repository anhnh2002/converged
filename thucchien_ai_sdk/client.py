"""
Client module for ThucChien.ai API authentication and configuration.
"""

import os
from typing import Optional
import openai


class ThucChienClient:
    """
    Client for ThucChien.ai API.
    Handles authentication and configuration.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.thucchien.ai/v1"):
        """
        Initialize ThucChien.ai client.
        
        Args:
            api_key: API key for authentication. If not provided, will look for THUCCHIEN_API_KEY env var.
            base_url: Base URL for the API endpoint.
        """
        self.api_key = api_key or os.getenv("THUCCHIEN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it as an argument or set THUCCHIEN_API_KEY environment variable."
            )
        
        self.base_url = base_url
        
        # Configure OpenAI client for ThucChien.ai API
        openai.api_key = self.api_key
        openai.api_base = self.base_url
        
    def get_api_key(self) -> str:
        """Get the configured API key."""
        return self.api_key
    
    def get_base_url(self) -> str:
        """Get the configured base URL."""
        return self.base_url
    
    def __repr__(self):
        return f"ThucChienClient(base_url='{self.base_url}')"


def get_client(api_key: Optional[str] = None) -> ThucChienClient:
    """
    Convenience function to create and return a ThucChien.ai client.
    
    Args:
        api_key: API key for authentication.
        
    Returns:
        ThucChienClient instance
    """
    return ThucChienClient(api_key=api_key)

