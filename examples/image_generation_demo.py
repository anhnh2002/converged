"""
Image Generation Demo
Demonstrates image generation, editing, and variation capabilities.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from thucchien_ai_sdk import ThucChienClient, ImageGenerator


def demo_chat_based_image_generation():
    """Demo: Chat-based image generation using Gemini"""
    print("\n" + "=" * 80)
    print("DEMO 1: Chat-based Image Generation (Gemini)")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = "A futuristic cityscape at sunset, with flying cars and neon lights. High resolution, photorealistic, 8k"
    print(f"\nPrompt: {prompt}")
    print("Using gemini-2.5-flash-image-preview model...")
    
    try:
        result = img_gen.chat_generate_image(
            prompt=prompt,
            model="gemini-2.5-flash-image-preview",
            save_path="../outputs/chat_generated_city.png"
        )
        print(f"\n✓ Image generated via chat endpoint!")
        print(f"  Saved to: outputs/chat_generated_city.png")
        print(f"  Model: {result.get('model', 'N/A')}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_simple_text_to_image():
    """Demo: Simple text-to-image generation"""
    print("\n" + "=" * 80)
    print("DEMO 2: Simple Text-to-Image (DALL-E)")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = "A peaceful zen garden with cherry blossom trees, koi pond, and stone lanterns at sunset"
    print(f"\nPrompt: {prompt}")
    
    try:
        result = img_gen.text_to_image(
            prompt=prompt,
            model="imagen-4",
            quality="standard",
            save_path="../outputs/zen_garden.png"
        )
        print(f"\n✓ Image generated successfully!")
        print(f"  Saved to: outputs/zen_garden.png")
        if result.get('data', [{}])[0].get('revised_prompt'):
            print(f"  Revised prompt: {result['data'][0]['revised_prompt'][:100]}...")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_high_quality_image():
    """Demo: High quality image generation"""
    print("\n" + "=" * 80)
    print("DEMO 3: High Quality Image Generation")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = """A cyberpunk street scene at night in Tokyo:
    - Neon signs in Japanese reflecting on wet pavement
    - A figure in a long coat walking through the rain
    - Holographic advertisements floating in the air
    - Blade Runner aesthetic with vibrant colors
    - Highly detailed, cinematic, 8K quality"""
    
    print(f"\nPrompt: {prompt[:100]}...")
    
    try:
        result = img_gen.text_to_image(
            prompt=prompt,
            model="imagen-4",
            save_path="../outputs/cyberpunk_street.png"
        )
        print(f"\n✓ High quality image generated!")
        print(f"  Saved to: outputs/cyberpunk_street.png")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_multiple_variations():
    """Demo: Generate multiple image variations"""
    print("\n" + "=" * 80)
    print("DEMO 4: Multiple Image Variations")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = "A cute robot mascot character for a tech company, friendly and approachable"
    print(f"\nPrompt: {prompt}")
    print(f"Generating 4 variations...")
    
    try:
        result = img_gen.text_to_image(
            prompt=prompt,
            model="imagen-4",  # imagen-4 supports multiple images
            n=4,
            save_path="../outputs/robot_mascot.png"
        )
        print(f"\n✓ Generated {len(result.get('data', []))} variations!")
        print(f"  Saved to: outputs/robot_mascot_*.png")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_portrait_generation():
    """Demo: Portrait generation with specific style"""
    print("\n" + "=" * 80)
    print("DEMO 5: Portrait Generation")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = """Professional headshot portrait of a confident female CEO:
    - Age 35-40, business attire
    - Natural lighting, soft shadows
    - Neutral gray background
    - Professional photography style
    - Warm, approachable expression"""
    
    print(f"\nPrompt: {prompt[:80]}...")
    
    try:
        result = img_gen.text_to_image(
            prompt=prompt,
            model="imagen-4",
            quality="hd",
            style="natural",
            save_path="../outputs/professional_portrait.png"
        )
        print(f"\n✓ Portrait generated successfully!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_artistic_styles():
    """Demo: Generate images in different artistic styles"""
    print("\n" + "=" * 80)
    print("DEMO 6: Different Artistic Styles")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    base_scene = "A lighthouse on a rocky coast during a storm"
    
    styles = [
        ("oil painting, impressionist style", "impressionist"),
        ("watercolor painting, soft colors", "watercolor"),
        ("digital art, cyberpunk aesthetic", "digital"),
        ("vintage photograph, 1920s style", "vintage"),
    ]
    
    for style_desc, style_name in styles:
        prompt = f"{base_scene}, {style_desc}"
        print(f"\n{style_name.capitalize()} style: {prompt[:60]}...")
        
        try:
            result = img_gen.text_to_image(
                prompt=prompt,
                model="imagen-4",
                save_path=f"../outputs/lighthouse_{style_name}.png"
            )
            print(f"  ✓ Generated and saved")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def demo_product_photography():
    """Demo: Product photography style images"""
    print("\n" + "=" * 80)
    print("DEMO 7: Product Photography")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = """Professional product photography of a luxury watch:
    - Swiss mechanical watch with visible gears
    - Clean white background
    - Studio lighting with soft reflections
    - Macro lens detail
    - Premium, elegant presentation"""
    
    print(f"\nPrompt: {prompt[:80]}...")
    
    try:
        result = img_gen.text_to_image(
            prompt=prompt,
            model="imagen-4",
            quality="hd",
            save_path="../outputs/watch_product.png"
        )
        print(f"\n✓ Product photo generated!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_multi_turn_editing():
    """Demo: Multi-turn image editing session"""
    print("\n" + "=" * 80)
    print("DEMO 8: Multi-turn Image Editing Session")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    # Create an editing session
    session = img_gen.create_editing_session(model="imagen-4")
    
    print("\nStarting iterative image creation...")
    
    # Step 1: Initial image
    print("\n[Step 1] Generating initial room...")
    try:
        session.generate(
            prompt="A modern minimalist living room with large windows",
            save_path="../outputs/session_step1.png"
        )
        print("  ✓ Initial image created")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Step 2: Add furniture
    print("\n[Step 2] Adding furniture...")
    try:
        session.generate(
            prompt="The same modern minimalist living room with large windows, now with a grey sectional sofa and wooden coffee table",
            save_path="../outputs/session_step2.png"
        )
        print("  ✓ Furniture added")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Step 3: Add plants
    print("\n[Step 3] Adding plants...")
    try:
        session.generate(
            prompt="The same living room with sofa and coffee table, now with several potted plants by the windows",
            save_path="../outputs/session_step3.png"
        )
        print("  ✓ Plants added")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    history = session.get_history()
    print(f"\n✓ Editing session complete! {len(history)} steps in history")


def demo_fantasy_scene():
    """Demo: Fantasy scene generation"""
    print("\n" + "=" * 80)
    print("DEMO 9: Fantasy Scene Generation")
    print("=" * 80)
    
    client = ThucChienClient()
    img_gen = ImageGenerator(client)
    
    prompt = """A magical fantasy library inside an ancient tree:
    - Bookshelves carved into living wood
    - Glowing crystals providing warm light
    - Floating books and magical runes
    - Spiral staircase winding up inside the trunk
    - Enchanted, whimsical atmosphere
    - Rich details, fantasy art style"""
    
    print(f"\nPrompt: {prompt[:80]}...")
    
    try:
        result = img_gen.text_to_image(
            prompt=prompt,
            model="imagen-4",
            save_path="../outputs/fantasy_library.png"
        )
        print(f"\n✓ Fantasy scene created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Run all demos"""
    try:
        print("\n" + "=" * 80)
        print("ThucChien AI - Image Generation Demos")
        print("=" * 80)
        
        # Run all demos
        demo_chat_based_image_generation()
        demo_simple_text_to_image()
        demo_high_quality_image()
        demo_multiple_variations()
        demo_portrait_generation()
        demo_artistic_styles()
        demo_product_photography()
        demo_multi_turn_editing()
        demo_fantasy_scene()
        
        print("\n" + "=" * 80)
        print("All demos completed!")
        print("Check the outputs/ directory for generated images.")
        print("=" * 80 + "\n")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.\n")
    except Exception as e:
        print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

