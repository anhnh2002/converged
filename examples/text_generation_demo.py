"""
Text Generation Demo
Demonstrates various text generation capabilities including single-turn and multi-turn conversations.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from thucchien_ai_sdk import ThucChienClient, TextGenerator


def demo_simple_generation():
    """Demo: Simple text generation"""
    print("\n" + "=" * 80)
    print("DEMO 1: Simple Text Generation")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    prompt = "Write a haiku about artificial intelligence"
    print(f"\nPrompt: {prompt}")
    
    response = generator.generate(
        prompt=prompt,
        temperature=0.8,
        model="gemini-2.5-flash"
    )
    
    print(f"\nResponse:\n{response}")


def demo_with_system_message():
    """Demo: Generation with system message"""
    print("\n" + "=" * 80)
    print("DEMO 2: Generation with System Message")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    prompt = "What is machine learning?"
    print(f"\nPrompt: {prompt}")
    
    response = generator.generate(
        prompt=prompt,
        system_message="You are a patient teacher explaining concepts to a 10-year-old child. Use simple language and fun examples.",
        temperature=0.7
    )
    
    print(f"\nResponse:\n{response}")


def demo_multi_turn_conversation():
    """Demo: Multi-turn conversation"""
    print("\n" + "=" * 80)
    print("DEMO 3: Multi-turn Conversation")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    # Create conversation
    conversation = generator.create_conversation(
        system_message="You are a knowledgeable Python programming tutor.",
        model="gemini-2.5-flash"
    )
    
    # Turn 1
    print("\n[User]: What are list comprehensions in Python?")
    response1 = conversation.send("What are list comprehensions in Python?")
    print(f"[Assistant]: {response1}")
    
    # Turn 2
    print("\n[User]: Can you show me an example?")
    response2 = conversation.send("Can you show me an example?")
    print(f"[Assistant]: {response2}")
    
    # Turn 3
    print("\n[User]: How is that different from a regular for loop?")
    response3 = conversation.send("How is that different from a regular for loop?")
    print(f"[Assistant]: {response3}")
    
    # Show history
    history = conversation.get_history()
    print(f"\n[Info]: Conversation has {len(history)} messages in history")


def demo_code_generation():
    """Demo: Code generation"""
    print("\n" + "=" * 80)
    print("DEMO 4: Code Generation")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    prompt = """Write a Python function that:
1. Takes a list of dictionaries as input
2. Sorts them by a specified key
3. Returns the sorted list
4. Includes error handling and type hints"""
    
    print(f"\nPrompt:\n{prompt}")
    
    response = generator.generate(
        prompt=prompt,
        system_message="You are an expert Python developer. Write clean, well-documented code with type hints.",
        temperature=0.3,  # Lower temperature for more deterministic code
    )
    
    print(f"\nGenerated Code:\n{response}")


def demo_creative_writing():
    """Demo: Creative writing"""
    print("\n" + "=" * 80)
    print("DEMO 5: Creative Writing")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    prompt = "Write the opening paragraph of a science fiction novel set on a space station"
    print(f"\nPrompt: {prompt}")
    
    response = generator.generate(
        prompt=prompt,
        temperature=0.9,  # Higher temperature for creativity
        max_tokens=200
    )
    
    print(f"\nResponse:\n{response}")


def demo_streaming():
    """Demo: Streaming responses"""
    print("\n" + "=" * 80)
    print("DEMO 6: Streaming Response")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    messages = [
        {"role": "user", "content": "Tell me a short story about a robot learning to paint"}
    ]
    
    print("\nStreaming response:")
    print("-" * 80)
    
    stream = generator.chat(messages=messages, stream=True, temperature=0.8)
    
    for chunk in stream:
        if chunk.choices[0].delta.get("content"):
            content = chunk.choices[0].delta["content"]
            print(content, end="", flush=True)
    
    print("\n" + "-" * 80)


def demo_conversation_context():
    """Demo: Using conversation context"""
    print("\n" + "=" * 80)
    print("DEMO 7: Conversation Context")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = TextGenerator(client)
    
    conversation = generator.create_conversation(
        system_message="You are a helpful assistant.",
        model="gemini-2.5-flash"
    )
    
    print("\n[User]: My favorite color is blue.")
    response1 = conversation.send("My favorite color is blue.")
    print(f"[Assistant]: {response1}")
    
    print("\n[User]: I also love the ocean.")
    response2 = conversation.send("I also love the ocean.")
    print(f"[Assistant]: {response2}")
    
    print("\n[User]: Can you recommend something based on what I told you?")
    response3 = conversation.send("Can you recommend something based on what I told you?")
    print(f"[Assistant]: {response3}")


def main():
    """Run all demos"""
    try:
        print("\n" + "=" * 80)
        print("ThucChien AI - Text Generation Demos")
        print("=" * 80)
        
        # Run all demos
        demo_simple_generation()
        demo_with_system_message()
        demo_multi_turn_conversation()
        demo_code_generation()
        demo_creative_writing()
        demo_streaming()
        demo_conversation_context()
        
        print("\n" + "=" * 80)
        print("All demos completed!")
        print("=" * 80 + "\n")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.\n")
    except Exception as e:
        print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

