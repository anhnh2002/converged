#!/usr/bin/env python3
"""
Simple example for video generation using ThucChien.ai SDK.

This demonstrates:
1. Text-to-video generation
2. Image-to-video generation
3. Video generation with first and last frame
"""

import os
from thucchien_ai_sdk import ThucChienClient, VeoVideoGenerator


def main():
    # Initialize client
    client = ThucChienClient()
    video_gen = VeoVideoGenerator(client)
    
    # Create output directory
    os.makedirs("outputs", exist_ok=True)
    
    print("=" * 60)
    print("VIDEO GENERATION EXAMPLES")
    print("=" * 60)
    
    # Example 1: Text-to-video generation
    print("\n1️⃣  Text-to-Video Generation")
    print("-" * 60)
    prompt = "A peaceful ocean sunset with waves gently rolling onto a sandy beach"
    print(f"Prompt: {prompt}")
    print("⏳ This will take a few minutes...")
    
    success = video_gen.generate_and_download(
        prompt=prompt,
        aspect_ratio="16:9",
        seed=42,
        output_path="outputs/text_to_video.mp4"
    )
    
    if success:
        print("✅ Text-to-video completed")
    else:
        print("❌ Text-to-video failed")
    
    # Example 2: Image-to-video generation
    print("\n2️⃣  Image-to-Video Generation")
    print("-" * 60)
    
    # Check if we have a generated image from the image generation example
    if os.path.exists("outputs/standard_image_1.png"):
        img_to_vid_prompt = "Animate this scene with gentle movements, clouds moving slowly across the sky"
        print(f"Prompt: {img_to_vid_prompt}")
        print("⏳ This will take a few minutes...")
        
        success = video_gen.generate_and_download(
            prompt=img_to_vid_prompt,
            image="outputs/standard_image_1.png",
            aspect_ratio="16:9",
            seed=123,
            output_path="outputs/image_to_video.mp4"
        )
        
        if success:
            print("✅ Image-to-video completed")
        else:
            print("❌ Image-to-video failed")
    else:
        print("⚠️  No image found for image-to-video. Run image_generation_example.py first.")
    
    print("\n" + "=" * 60)
    print("✨ All examples completed!")
    print(f"📁 Check the 'outputs' folder for generated videos")
    print("=" * 60)


if __name__ == "__main__":
    main()

