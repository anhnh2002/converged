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
        model: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        system_message: Optional[str] = None,
    ) -> str:
        """
        Generate text from a single prompt.
        
        Args:
            prompt: The text prompt to generate from
            model: Model to use (gemini-2.5-flash, gpt-4, etc.)
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
        model: str = "gemini-2.5-flash",
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


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_simple_generation(client: ThucChienClient):
    """Example: Simple text generation"""
    generator = TextGenerator(client)
    
    response = generator.generate(
        prompt="Write a short poem about artificial intelligence.",
        temperature=0.8,
    )
    
    print("Generated Text:")
    print(response)
    return response


def example_with_system_message(client: ThucChienClient):
    """Example: Generation with system message"""
    generator = TextGenerator(client)
    
    response = generator.generate(
        prompt="Explain quantum computing in simple terms.",
        system_message="You are a patient teacher explaining complex topics to beginners.",
        temperature=0.7,
    )
    
    print("Generated Text:")
    print(response)
    return response


def example_multi_turn_conversation(client: ThucChienClient):
    """Example: Multi-turn conversation"""
    generator = TextGenerator(client)
    
    # Create a conversation
    conversation = generator.create_conversation(
        system_message="You are a helpful coding assistant.",
        model="gemini-2.5-flash",
    )
    
    # First turn
    response1 = conversation.send("What is a Python decorator?")
    print(f"User: What is a Python decorator?")
    print(f"Assistant: {response1}\n")
    
    # Second turn (with context from first)
    response2 = conversation.send("Can you show me an example?")
    print(f"User: Can you show me an example?")
    print(f"Assistant: {response2}\n")
    
    # Third turn
    response3 = conversation.send("How is this different from a function wrapper?")
    print(f"User: How is this different from a function wrapper?")
    print(f"Assistant: {response3}\n")
    
    # Get full history
    history = conversation.get_history()
    print(f"Total messages in history: {len(history)}")
    
    return history


def example_streaming_response(client: ThucChienClient):
    """Example: Streaming text generation"""
    generator = TextGenerator(client)
    
    messages = [
        {"role": "user", "content": "Write a short story about a robot learning to paint."}
    ]
    
    print("Streaming response:")
    stream = generator.chat(messages=messages, stream=True)
    
    for chunk in stream:
        if chunk.choices[0].delta.get("content"):
            content = chunk.choices[0].delta["content"]
            print(content, end="", flush=True)
    
    print("\n")


def example_code_generation(client: ThucChienClient):
    """Example: Code generation with specific parameters"""
    generator = TextGenerator(client)
    
    response = generator.generate(
        prompt="""Write a Python function that:
1. Takes a list of numbers as input
2. Returns a dictionary with 'mean', 'median', and 'mode'
3. Includes error handling for empty lists
4. Has proper docstring and type hints""",
        system_message="You are an expert Python developer who writes clean, well-documented code.",
        temperature=0.3,  # Lower temperature for more deterministic code
        model="gpt-4",
    )
    
    print("Generated Code:")
    print(response)
    return response


if __name__ == "__main__":
    # Example usage (requires API key in environment)
    try:
        client = ThucChienClient()
        
        print("=" * 80)
        print("Example 1: Simple Generation")
        print("=" * 80)
        example_simple_generation(client)
        
        print("\n" + "=" * 80)
        print("Example 2: Multi-turn Conversation")
        print("=" * 80)
        example_multi_turn_conversation(client)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.")

