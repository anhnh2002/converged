#!/usr/bin/env python3
"""
Simple example for image generation using ThucChien.ai SDK.

This demonstrates:
1. Text-to-image generation
2. Chat-based image generation
3. Image editing
"""

import os
from thucchien_ai_sdk import ThucChienClient, StandardImageGenerator, ConversationalImageGenerator
from thucchien_ai_sdk.utils import to_base64


def main():
    # Initialize client
    client = ThucChienClient()
    
    # Initialize generators
    standard_gen = StandardImageGenerator(client)
    conversational_gen = ConversationalImageGenerator(client)
    
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
    
    # images = standard_gen.standard_generate_image(
    #     prompt=prompt,
    #     n=1,
    #     aspect_ratio="16:9",
    #     save_path="outputs/standard_image.png"
    # )
    # print(f"✅ Generated {len(images)} image(s)")
    
    # # Example 2: Conversational image generation (single image)
    # print("\n2️⃣  Conversational Image Generation")
    # print("-" * 60)
    # chat_prompt = "A futuristic city with flying cars and tall skyscrapers"
    # print(f"Prompt: {chat_prompt}")
    
    # base64_data, mime_type = conversational_gen.generate(
    #     prompt=chat_prompt,
    #     aspect_ratio="16:9",
    #     save_path="outputs/chat_image.png"
    # )
    # print("✅ Conversational image generated")
    
    # # Example 3: Image editing (requires an existing image)
    # print("\n3️⃣  Image Editing")
    # print("-" * 60)
    
    # # First, check if we have an image to edit
    # if os.path.exists("outputs/standard_image.png"):
    #     edit_prompt = "Add a small boat on the lake"
    #     print(f"Edit prompt: {edit_prompt}")
        
    #     # Convert existing image to base64
    #     existing_image_b64, existing_mime_type = to_base64("outputs/standard_image.png")
        
    #     # Edit the image using conversational generator
    #     edited_b64, edited_mime = conversational_gen.generate(
    #         prompt=edit_prompt,
    #         prev_contents=[
    #             {
    #                 "role": "user", 
    #                 "parts": [{"inlineData": {"mime_type": existing_mime_type, "data": existing_image_b64}}]
    #             },
    #         ],
    #         aspect_ratio="16:9",
    #         save_path="outputs/edited_image.png"
    #     )
    #     print("✅ Image edited successfully")
    # else:
    #     print("⚠️  No image found to edit. Run standard generation first.")
    
    # Example 4: Multi-turn conversation - Generate consistent character across multiple images
    print("\n4️⃣  Multi-turn Conversation (Consistent Character Storyboard)")
    print("-" * 60)
    print("Generating a news report storyboard with consistent reporter...")
    
    # Image 1: Reporter portrait
    reporter_portrait_prompt = "A close-up portrait of the reporter standing in front of a newsroom backdrop. Add an on-screen lower-third text: 'Maria Chen - Senior Field Correspondent, Global News.' She wears a professional outfit (navy blazer, press badge, holding microphone with network logo). Calm and confident expression, ready to report."
    print(f"\n  📸 Image 1: Reporter portrait")
    reporter_portrait_base64, reporter_portrait_mime_type = conversational_gen.generate(
        prompt=reporter_portrait_prompt,
        aspect_ratio="16:9",
        save_path="outputs/reporter_portrait.png"
    )
    print("  ✅ Reporter portrait generated")
    
    # Image 2: Reporter sitting at the anchor desk
    reporter_sitting_prompt = "The reporter sits at the anchor desk in a modern TV studio. Multiple display screens show world maps and headlines. Bright, professional lighting and sleek digital graphics in the background."
    print(f"\n  📸 Image 2: Reporter at anchor desk")
    reporter_sitting_base64, reporter_sitting_mime_type = conversational_gen.generate(
        prompt=reporter_sitting_prompt,
        prev_contents=[
            {"role": "user", "parts": [{"text": reporter_portrait_prompt}]},
            {"role": "model", "parts": [{"inlineData": {"mime_type": reporter_portrait_mime_type, "data": reporter_portrait_base64}}]},
        ],
        aspect_ratio="16:9",
        save_path="outputs/reporter_sitting.png"
    )
    print("  ✅ Reporter at anchor desk generated")
    
    # Image 3: Reporter reacting to urgent breaking news
    reporter_breaking_news_prompt = "The same reporter reacts to urgent breaking news. Red 'BREAKING NEWS' graphics flash behind her as she looks at a monitor, microphone on desk. Serious, focused demeanor."
    print(f"\n  📸 Image 3: Reporter with breaking news")
    reporter_breaking_news_base64, reporter_breaking_news_mime_type = conversational_gen.generate(
        prompt=reporter_breaking_news_prompt,
        prev_contents=[
            {"role": "user", "parts": [{"text": reporter_portrait_prompt}]},
            {"role": "model", "parts": [{"inlineData": {"mime_type": reporter_portrait_mime_type, "data": reporter_portrait_base64}}]},
            {"role": "user", "parts": [{"text": reporter_sitting_prompt}]},
            {"role": "model", "parts": [{"inlineData": {"mime_type": reporter_sitting_mime_type, "data": reporter_sitting_base64}}]},
        ],
        aspect_ratio="16:9",
        save_path="outputs/reporter_breaking_news.png"
    )
    print("  ✅ Reporter with breaking news generated")
    print("\n✅ Multi-turn storyboard completed with consistent character!")
    
    print("\n" + "=" * 60)
    print("✨ All examples completed!")
    print(f"📁 Check the 'outputs' folder for generated images")
    print("=" * 60)


if __name__ == "__main__":
    main()

