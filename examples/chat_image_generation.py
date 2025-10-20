"""
Chat-based Image Generation Demo
Demonstrates the Gemini chat endpoint for image generation.

This method uses the /chat/completions endpoint with gemini-2.5-flash-image-preview model
to generate images directly within a conversation. Images are returned as base64-encoded data.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from thucchien_ai_sdk import ThucChienClient, ImageGenerator


def demo_basic_chat_image():
    """Basic chat-based image generation"""
    print("\n" + "=" * 80)
    print("Chat-based Image Generation - Basic Example")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = """A futuristic cityscape at sunset, with flying cars and neon lights. 
    High resolution, photorealistic, 8k"""
    
    print(f"\nPrompt: {prompt}")
    print("Model: gemini-2.5-flash-image-preview")
    print("Endpoint: /chat/completions")
    print("\nGenerating image...")
    
    try:
        result = img_gen.chat_generate_image(
            prompt=prompt,
            model="gemini-2.5-flash-image-preview",
            save_path="../outputs/chat_futuristic_city.png"
        )
        
        print("\n✓ Success!")
        print(f"  Image saved to: outputs/chat_futuristic_city.png")
        print(f"  Response format: Base64-encoded")
        
        # Show response structure
        if 'choices' in result:
            print(f"  Choices: {len(result['choices'])}")
            print(f"  Model: {result.get('model', 'N/A')}")
        
        return result
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


def demo_multi_turn_chat_images():
    """Multi-turn conversation with image refinement"""
    print("\n" + "=" * 80)
    print("Chat-based Image Generation - Multi-turn Conversation")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    # First image generation
    print("\n[Turn 1] Initial image generation:")
    messages = []
    prompt1 = "Create a serene landscape with mountains and a lake"
    
    print(f"Prompt: {prompt1}")
    
    try:
        result1 = img_gen.chat_generate_image(
            prompt=prompt1,
            model="gemini-2.5-flash-image-preview",
            messages=messages.copy(),
            save_path="../outputs/chat_turn1.png"
        )
        print("✓ Image 1 saved to: outputs/chat_turn1.png")
        
        # Build conversation history for next turn
        # Note: In a real multi-turn scenario, you'd preserve the full conversation
        messages.append({"role": "user", "content": prompt1})
        if 'choices' in result1:
            messages.append({
                "role": "assistant",
                "content": result1['choices'][0]['message'].get('content', '')
            })
        
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_different_styles():
    """Generate images in different styles using chat endpoint"""
    print("\n" + "=" * 80)
    print("Chat-based Image Generation - Different Styles")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    styles = [
        ("A majestic dragon, fantasy art style, detailed scales", "fantasy"),
        ("A modern office space, minimalist design, photorealistic", "modern"),
        ("A vintage car, 1950s style, nostalgic atmosphere", "vintage"),
        ("An abstract composition, vibrant colors, modern art", "abstract"),
    ]
    
    print(f"\nGenerating {len(styles)} images in different styles...\n")
    
    for prompt, style_name in styles:
        print(f"Style: {style_name}")
        print(f"Prompt: {prompt[:60]}...")
        
        try:
            result = img_gen.chat_generate_image(
                prompt=prompt,
                model="gemini-2.5-flash-image-preview",
                save_path=f"../outputs/chat_style_{style_name}.png"
            )
            print(f"  ✓ Saved to: outputs/chat_style_{style_name}.png\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")


def demo_high_detail_prompt():
    """Generate with highly detailed prompt"""
    print("\n" + "=" * 80)
    print("Chat-based Image Generation - High Detail Prompt")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = """
    Create a highly detailed scene:
    - Setting: A cozy library in an old castle
    - Time: Late evening with warm candlelight
    - Elements: 
      * Tall wooden bookshelves filled with ancient books
      * A reading nook with a leather armchair
      * A globe on an antique desk
      * Arched windows showing a starry night sky
      * Persian rug on stone floor
    - Style: Photorealistic, cinematic lighting
    - Mood: Warm, inviting, mysterious
    - Quality: High resolution, 8K, highly detailed
    """
    
    print("\nGenerating with detailed prompt...")
    print(f"Prompt length: {len(prompt)} characters")
    
    try:
        result = img_gen.chat_generate_image(
            prompt=prompt,
            model="gemini-2.5-flash-image-preview",
            save_path="../outputs/chat_detailed_library.png"
        )
        
        print("\n✓ High-detail image generated!")
        print(f"  Saved to: outputs/chat_detailed_library.png")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_comparison_with_dalle():
    """Compare Gemini chat-based vs DALL-E generation"""
    print("\n" + "=" * 80)
    print("Comparison: Gemini Chat vs DALL-E")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = "A peaceful zen garden with a koi pond and cherry blossoms"
    
    # Gemini Chat-based
    print("\n[Method 1] Gemini Chat-based (gemini-2.5-flash-image-preview)")
    print(f"  Endpoint: /chat/completions")
    print(f"  Response: Base64-encoded")
    
    try:
        result1 = img_gen.chat_generate_image(
            prompt=prompt,
            model="gemini-2.5-flash-image-preview",
            save_path="../outputs/comparison_gemini.png"
        )
        print("  ✓ Generated: outputs/comparison_gemini.png")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # DALL-E
    print("\n[Method 2] DALL-E 3")
    print(f"  Endpoint: /images/generations")
    print(f"  Response: URL or base64")
    
    try:
        result2 = img_gen.text_to_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024",
            save_path="../outputs/comparison_dalle.png"
        )
        print("  ✓ Generated: outputs/comparison_dalle.png")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n" + "-" * 80)
    print("Key Differences:")
    print("  Gemini: Conversational, multi-turn capable, base64 inline")
    print("  DALL-E: Single-shot, URL-based, more style control")


def main():
    """Run all chat-based image generation demos"""
    try:
        print("\n" + "=" * 80)
        print("ThucChien AI - Chat-based Image Generation Demos")
        print("Using Gemini 2.5 Flash Image Preview Model")
        print("=" * 80)
        
        # Run demos
        demo_basic_chat_image()
        demo_multi_turn_chat_images()
        demo_different_styles()
        demo_high_detail_prompt()
        demo_comparison_with_dalle()
        
        print("\n" + "=" * 80)
        print("All demos completed!")
        print("Check the outputs/ directory for generated images.")
        print("=" * 80)
        
        print("\n" + "=" * 80)
        print("Key Features of Chat-based Image Generation:")
        print("=" * 80)
        print("1. Uses /chat/completions endpoint")
        print("2. Model: gemini-2.5-flash-image-preview")
        print("3. Returns base64-encoded images in chat response")
        print("4. Supports multi-turn conversations")
        print("5. Good for conversational workflows")
        print("6. Images extracted from: result['choices'][0]['message']['images'][0]")
        print("=" * 80 + "\n")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.\n")
    except Exception as e:
        print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

