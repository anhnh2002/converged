"""
Text generation module with multi-turn conversation support.
"""

from typing import List, Dict, Optional, Any
import openai
from .client import ThucChienClient


class TextGenerator:
    """
    Text generation with support for single-turn and multi-turn conversations.
    """
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize TextGenerator with a ThucChien.ai client.
        
        Args:
            client: ThucChienClient instance
        """
        self.client = client
        self.openai_client = openai.OpenAI(api_key=client.get_api_key(), base_url=client.get_base_url())
        
    def generate(
        self,
        prompt: str,
        model: str = "gemini-2.5-pro",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        system_message: Optional[str] = None,
    ) -> str:
        """
        Generate text from a single prompt.
        
        Args:
            prompt: The text prompt to generate from
            model: Model to use (gemini-2.5-flash, gemini-2.5-pro)
            temperature: Controls randomness (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            system_message: Optional system message to set context
            
        Returns:
            Generated text response
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        
        return response.choices[0].message.content
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-2.5-pro",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        stream: bool = False,
    ) -> Any:
        """
        Multi-turn conversation with message history.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                      Role can be 'system', 'user', or 'assistant'
            model: Model to use
            temperature: Controls randomness
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            stream: Whether to stream the response
            
        Returns:
            Generated response (str if not streaming, generator if streaming)
        """
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
        )
        
        if stream:
            return response
        else:
            return response.choices[0].message.content
    
    def create_conversation(
        self,
        system_message: Optional[str] = None,
        model: str = "gemini-2.5-flash",
    ) -> 'Conversation':
        """
        Create a conversation session for multi-turn interactions.
        
        Args:
            system_message: Optional system message to set conversation context
            model: Model to use for the conversation
            
        Returns:
            Conversation instance
        """
        return Conversation(self, system_message=system_message, model=model)


class Conversation:
    """
    Manages multi-turn conversations with message history.
    """
    
    def __init__(
        self,
        text_generator: TextGenerator,
        system_message: Optional[str] = None,
        model: str = "gemini-2.5-flash",
    ):
        """
        Initialize a conversation session.
        
        Args:
            text_generator: TextGenerator instance
            system_message: Optional system message
            model: Model to use
        """
        self.text_generator = text_generator
        self.model = model
        self.messages: List[Dict[str, str]] = []
        
        if system_message:
            self.messages.append({"role": "system", "content": system_message})
    
    def send(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Send a message in the conversation and get a response.
        
        Args:
            message: User message to send
            temperature: Controls randomness
            max_tokens: Maximum tokens to generate
            
        Returns:
            Assistant's response
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": message})
        
        # Get response
        response = self.text_generator.chat(
            messages=self.messages,
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Add assistant response to history
        self.messages.append({"role": "assistant", "content": response})
        
        return response
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.messages.copy()
    
    def clear_history(self, keep_system: bool = True):
        """
        Clear conversation history.
        
        Args:
            keep_system: Whether to keep the system message
        """
        if keep_system and self.messages and self.messages[0]["role"] == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []
    
    def __repr__(self):
        return f"Conversation(model='{self.model}', messages={len(self.messages)})"




