"""
Video Generation Demo
Demonstrates text-to-video and image-to-video capabilities.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from thucchien_ai_sdk import ThucChienClient, VideoGenerator


def demo_simple_text_to_video():
    """Demo: Simple text-to-video generation"""
    print("\n" + "=" * 80)
    print("DEMO 1: Simple Text-to-Video")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = "A beautiful sunset over the ocean, waves gently rolling onto the beach"
    print(f"\nPrompt: {prompt}")
    print("Generating video (this may take a few minutes)...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=5,
            resolution="1080p",
            aspect_ratio="16:9",
            save_path="../outputs/ocean_sunset.mp4",
            poll_interval=10
        )
        print(f"\n✓ Video generated successfully!")
        print(f"  Saved to: outputs/ocean_sunset.mp4")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_cinematic_shot():
    """Demo: Cinematic video with camera movement"""
    print("\n" + "=" * 80)
    print("DEMO 2: Cinematic Shot with Camera Movement")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """A smooth tracking shot following a sports car driving through 
    a neon-lit cyberpunk city at night. The camera dollies alongside the car 
    as it weaves through traffic, holographic billboards reflecting off the 
    wet pavement, rain falling, bokeh effect from city lights, 
    vibrant purple and blue color grading, cinematic."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating cinematic video...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=8,
            resolution="1080p",
            aspect_ratio="16:9",
            fps=30,
            save_path="../outputs/cyberpunk_chase.mp4"
        )
        print(f"\n✓ Cinematic video created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_video_with_dialogue():
    """Demo: Video with dialogue and sound effects"""
    print("\n" + "=" * 80)
    print("DEMO 3: Video with Dialogue")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """Two astronauts in a space station looking at Earth through a large window.
    "It never gets old, does it?" the first astronaut says softly.
    "Never," the second replies, smiling.
    Soft blue lighting from Earth's reflection, stars visible in the background,
    peaceful atmosphere, cinematic composition."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating video with dialogue...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=6,
            resolution="1080p",
            save_path="../outputs/astronaut_dialogue.mp4"
        )
        print(f"\n✓ Video with dialogue created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_animated_character():
    """Demo: 3D animated character video"""
    print("\n" + "=" * 80)
    print("DEMO 4: 3D Animated Character")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """A cute 3D animated dragon character with big eyes, 
    happily bouncing through a magical forest. The dragon discovers a glowing 
    crystal and tilts its head in curiosity. Pixar-style animation, 
    bright cheerful colors, soft lighting, whimsical atmosphere."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating animated character video...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=6,
            resolution="1080p",
            save_path="../outputs/cute_dragon.mp4"
        )
        print(f"\n✓ Animated character video created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_product_showcase():
    """Demo: Product showcase video"""
    print("\n" + "=" * 80)
    print("DEMO 5: Product Showcase Video")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """A sleek modern smartphone rotating on a white pedestal 
    against a minimalist white background. Studio lighting with soft shadows, 
    the phone screen displays a vibrant colorful interface, 
    camera slowly orbits around the product, professional product photography style, 
    clean and premium aesthetic."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating product showcase...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=5,
            resolution="1080p",
            save_path="../outputs/phone_showcase.mp4"
        )
        print(f"\n✓ Product showcase video created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_nature_documentary():
    """Demo: Nature documentary style video"""
    print("\n" + "=" * 80)
    print("DEMO 6: Nature Documentary Style")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """A serene nature scene: a family of deer grazing in a misty meadow 
    at dawn, golden sunlight filtering through the trees, 
    gentle fog rolling across the grass, birds flying in the background, 
    documentary style cinematography, peaceful and tranquil atmosphere."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating nature documentary video...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=8,
            resolution="1080p",
            save_path="../outputs/nature_deer.mp4"
        )
        print(f"\n✓ Nature documentary video created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_action_sequence():
    """Demo: Action sequence video"""
    print("\n" + "=" * 80)
    print("DEMO 7: Action Sequence")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """An action-packed scene of a parkour athlete jumping between 
    rooftops in an urban environment. Dynamic camera following the action, 
    fast-paced movement, dramatic angles, city skyline in background, 
    golden hour lighting, motion blur on background, 
    adrenaline-pumping athletic performance."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating action sequence...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=6,
            resolution="1080p",
            fps=30,
            save_path="../outputs/parkour_action.mp4"
        )
        print(f"\n✓ Action sequence created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_vertical_video():
    """Demo: Vertical video for social media"""
    print("\n" + "=" * 80)
    print("DEMO 8: Vertical Video (Social Media)")
    print("=" * 80)
    
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = """A trendy coffee art video: barista's hands creating a beautiful 
    latte art pattern in a white cup, viewed from above, 
    warm cafe atmosphere, soft natural lighting, 
    Instagram-worthy aesthetic, appealing and satisfying."""
    
    print(f"\nPrompt: {prompt[:100]}...")
    print("Generating vertical video...")
    
    try:
        result = video_gen.text_to_video(
            prompt=prompt,
            model="veo-3",
            duration=5,
            resolution="1080p",
            aspect_ratio="9:16",  # Vertical for social media
            save_path="../outputs/latte_art_vertical.mp4"
        )
        print(f"\n✓ Vertical video created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_image_to_video():
    """Demo: Animate a still image"""
    print("\n" + "=" * 80)
    print("DEMO 9: Image-to-Video Animation")
    print("=" * 80)
    print("\nNote: This demo requires an input image.")
    print("Skipping for now. To run this demo:")
    print("1. Place an image at: ../outputs/input_image.jpg")
    print("2. Uncomment the code below")
    
    # Uncomment to run when you have an input image:
    """
    client = ThucChienClient()
    video_gen = VideoGenerator(client)
    
    prompt = "The clouds slowly drift across the sky, trees sway gently in the breeze"
    
    try:
        result = video_gen.image_to_video(
            image_path="../outputs/input_image.jpg",
            prompt=prompt,
            duration=5,
            motion_strength=0.7,
            save_path="../outputs/animated_scene.mp4"
        )
        print(f"\n✓ Image animated successfully!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    """


def main():
    """Run all demos"""
    try:
        print("\n" + "=" * 80)
        print("ThucChien AI - Video Generation Demos")
        print("=" * 80)
        print("\nWARNING: Video generation can take several minutes per video.")
        print("Some demos may be skipped to save time.")
        print("Uncomment specific demos in the code to run them.")
        
        # Run selected demos (uncomment others as needed)
        demo_simple_text_to_video()
        # demo_cinematic_shot()
        # demo_video_with_dialogue()
        # demo_animated_character()
        # demo_product_showcase()
        # demo_nature_documentary()
        # demo_action_sequence()
        # demo_vertical_video()
        demo_image_to_video()
        
        print("\n" + "=" * 80)
        print("Selected demos completed!")
        print("Check the outputs/ directory for generated videos.")
        print("=" * 80 + "\n")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.\n")
    except Exception as e:
        print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

