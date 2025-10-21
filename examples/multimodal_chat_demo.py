#!/usr/bin/env python3
"""
Multimodal Chat Demo
Demonstrates programmatic usage of the multimodal chat API with text and images.
"""

import os
import sys

# Add parent directory to path to import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thucchien_ai_sdk import ThucChienClient
from thucchien_ai_sdk.image_generation import ImageGenerator


def demo_basic_image_generation():
    """Demo: Basic image generation with aspect ratio."""
    print("=" * 80)
    print("DEMO 1: Basic Image Generation with Aspect Ratio")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = ImageGenerator(client)
    
    # Create a conversation
    conversation = generator.create_conversation(
        system_message="You are a creative AI assistant that helps generate beautiful images."
    )
    
    # Generate an image with 16:9 aspect ratio
    print("\n📝 Request: Generate a landscape image (16:9)")
    result = conversation.send(
        text="Create a beautiful landscape of mountains at sunset",
        aspect_ratio="16:9",
        save_path="outputs/chat_session/landscape_16_9.png"
    )
    
    # Check response
    if 'choices' in result and result['choices']:
        message = result['choices'][0]['message']
        if 'content' in message:
            print(f"🤖 Response: {message['content']}")
        if 'images' in message and message['images']:
            print(f"✅ Generated {len(message['images'])} image(s)")
    
    print()



def demo_multi_turn_conversation():
    """Demo: Multi-turn conversation with context."""
    print("=" * 80)
    print("DEMO 3: Multi-turn Conversation")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = ImageGenerator(client)
    
    # Create conversation
    conversation = generator.create_conversation()
    
    # Turn 1: Generate initial image
    print("\n💬 Turn 1: Generate a cat")
    result1 = conversation.send(
        text="Create an image of a cute orange cat",
        aspect_ratio="1:1",
        save_path="outputs/chat_session/cat_v1.png"
    )
    print(f"✅ Image generated: outputs/chat_session/cat_v1.png")
    
    # Turn 2: Modify the image (using context)
    print("\n💬 Turn 2: Add a hat")
    result2 = conversation.send(
        text="Now add a wizard hat to the cat",
        aspect_ratio="1:1",
        save_path="outputs/chat_session/cat_v2.png"
    )
    print(f"✅ Modified image: outputs/chat_session/cat_v2.png")
    
    # Turn 3: Further modification
    print("\n💬 Turn 3: Add background")
    result3 = conversation.send(
        text="Add a magical forest background",
        aspect_ratio="1:1",
        save_path="outputs/chat_session/cat_v3.png"
    )
    print(f"✅ Final image: outputs/chat_session/cat_v3.png")
    
    # Show conversation stats
    history = conversation.get_history()
    print(f"\n📊 Conversation stats: {len(history)} messages exchanged")
    
    print()


def demo_with_input_image():
    """Demo: Chat with input image."""
    print("=" * 80)
    print("DEMO 4: Chat with Input Image")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = ImageGenerator(client)
    
    # Check if there's an existing image to use
    test_images = [
        "outputs/mountain.png",
        "outputs/mountain-2.png",
        "outputs/mountain-3.png"
    ]
    
    existing_image = None
    for img in test_images:
        if os.path.exists(img):
            existing_image = img
            break
    
    if existing_image:
        print(f"\n📎 Using existing image: {existing_image}")
        
        # Analyze the image
        conversation = generator.create_conversation()
        
        result = conversation.send(
            text="Describe this image and create a similar one with a sunset instead",
            image_paths=[existing_image],
            aspect_ratio="16:9",
            save_path="outputs/chat_session/modified_scene.png"
        )
        
        if 'choices' in result and result['choices']:
            message = result['choices'][0]['message']
            if 'content' in message:
                print(f"\n🤖 Response: {message['content']}")
        
        print()
    else:
        print("\n⚠️  No existing images found to demo with. Skipping this demo.")
        print("   (Generate some images first using other demos)")
        print()


def demo_portrait_and_landscape():
    """Demo: Portrait and landscape orientations."""
    print("=" * 80)
    print("DEMO 5: Portrait vs Landscape")
    print("=" * 80)
    
    client = ThucChienClient()
    generator = ImageGenerator(client)
    
    # Portrait (9:16)
    print("\n📱 Creating portrait image (9:16)")
    generator.chat_generate_image(
        prompt="A tall waterfall in a lush forest, vertical composition",
        aspect_ratio="9:16",
        save_path="outputs/chat_session/waterfall_portrait.png"
    )
    print("✅ Portrait saved: outputs/chat_session/waterfall_portrait.png")
    
    # Landscape (16:9)
    print("\n🖼️  Creating landscape image (16:9)")
    generator.chat_generate_image(
        prompt="A wide panoramic view of a desert at golden hour",
        aspect_ratio="16:9",
        save_path="outputs/chat_session/desert_landscape.png"
    )
    print("✅ Landscape saved: outputs/chat_session/desert_landscape.png")
    
    # Square (1:1)
    print("\n⬛ Creating square image (1:1)")
    generator.chat_generate_image(
        prompt="A balanced composition of a single rose in a vase",
        aspect_ratio="1:1",
        save_path="outputs/chat_session/rose_square.png"
    )
    print("✅ Square saved: outputs/chat_session/rose_square.png")
    
    print()


def main():
    """Run all demos."""
    try:
        # Create output directory
        os.makedirs("outputs/chat_session", exist_ok=True)
        
        print("\n🎨 MULTIMODAL CHAT API DEMOS 🎨\n")
        
        # Run demos
        demo_basic_image_generation()
        demo_multi_turn_conversation()
        demo_with_input_image()
        demo_portrait_and_landscape()
        
        print("=" * 80)
        print("✅ ALL DEMOS COMPLETED!")
        print("=" * 80)
        print("\nGenerated images are in: outputs/chat_session/")
        print("\nTo try the interactive terminal chat, run:")
        print("  python examples/multimodal_chat_terminal.py")
        print()
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

