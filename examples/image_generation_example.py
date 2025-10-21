#!/usr/bin/env python3
"""
Simple example for image generation using ThucChien.ai SDK.

This demonstrates:
1. Text-to-image generation
2. Chat-based image generation
3. Image editing
"""

import os
from thucchien_ai_sdk import ThucChienClient, ImageGenerator
from thucchien_ai_sdk.image_generation import ImageEditor


def main():
    # Initialize client
    client = ThucChienClient()
    image_gen = ImageGenerator(client)
    image_editor = ImageEditor(client)
    
    # Create output directory
    os.makedirs("outputs", exist_ok=True)
    
    print("=" * 60)
    print("IMAGE GENERATION EXAMPLES")
    print("=" * 60)
    
    # # Example 1: Standard text-to-image generation
    # print("\n1️⃣  Standard Image Generation")
    # print("-" * 60)
    # prompt = "A serene mountain landscape at sunset with a lake reflecting the sky"
    # print(f"Prompt: {prompt}")
    
    # images = image_gen.standard_generate_image(
    #     prompt=prompt,
    #     n=1,
    #     image_size="1k",
    #     aspect_ratio="16:9",
    #     save_path="outputs/standard_image"
    # )
    # print(f"✅ Generated {len(images)} image(s)")
    
    # # Example 2: Chat-based image generation
    # print("\n2️⃣  Chat-based Image Generation")
    # print("-" * 60)
    # chat_prompt = "Create a futuristic city with flying cars and tall skyscrapers"
    # print(f"Prompt: {chat_prompt}")
    
    # chat_image = image_gen.chat_generate_image(
    #     prompt=chat_prompt,
    #     save_path="outputs/chat_image.png"
    # )
    # print("✅ Chat-based image generated")
    
    # Example 3: Image editing (requires an existing image)
    print("\n3️⃣  Image Editing")
    print("-" * 60)
    
    # First, check if we have an image to edit
    if os.path.exists("outputs/standard_image_1.png"):
        edit_prompt = "Add a small boat on the lake"
        print(f"Edit prompt: {edit_prompt}")
        
        edited_image = image_editor.edit_image(
            prompt=edit_prompt,
            image="outputs/standard_image_1.png",
            aspect_ratio="16:9",
            save_path="outputs/edited_image.png"
        )
        print("✅ Image edited successfully")
    else:
        print("⚠️  No image found to edit. Run standard generation first.")
    
    print("\n" + "=" * 60)
    print("✨ All examples completed!")
    print(f"📁 Check the 'outputs' folder for generated images")
    print("=" * 60)


if __name__ == "__main__":
    main()

