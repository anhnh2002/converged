"""
Complete Creative Workflow Demo
Demonstrates a complete end-to-end workflow using multiple AI capabilities:
1. Generate a story concept with text generation
2. Create character images
3. Generate a video scene
4. Create audio narration
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from thucchien_ai_sdk import (
    ThucChienClient,
    TextGenerator,
    ImageGenerator,
    VideoGenerator,
    TextToSpeech
)


def workflow_story_creation():
    """
    Complete workflow: Create a short story with visuals and audio
    """
    print("\n" + "=" * 80)
    print("COMPLETE CREATIVE WORKFLOW DEMO")
    print("Creating a short story with visuals and audio")
    print("=" * 80)
    
    # Initialize client
    client = ThucChienClient()
    
    # =========================================================================
    # STEP 1: Generate Story Concept
    # =========================================================================
    print("\n[Step 1/4] Generating story concept...")
    print("-" * 80)
    
    text_gen = TextGenerator(client)
    
    story_prompt = """Create a short story concept (3-4 sentences) about:
    - A young astronaut discovering an ancient artifact on Mars
    - Include a description of the scene for visualization
    - Make it engaging and mysterious"""
    
    story = text_gen.generate(
        prompt=story_prompt,
        temperature=0.8,
        system_message="You are a creative science fiction writer."
    )
    
    print(f"\nGenerated Story:\n{story}\n")
    
    # =========================================================================
    # STEP 2: Create Character Image
    # =========================================================================
    print("\n[Step 2/4] Creating character visualization...")
    print("-" * 80)
    
    img_gen = ImageGenerator(client)
    
    character_prompt = """A young astronaut in a futuristic spacesuit, 
    standing on Mars surface, looking at a glowing ancient artifact in their hands,
    red desert landscape, dramatic lighting from two moons in the sky,
    cinematic, photorealistic, highly detailed"""
    
    try:
        character_result = img_gen.text_to_image(
            prompt=character_prompt,
            model="dall-e-3",
            size="1024x1024",
            quality="hd",
            save_path="../outputs/workflow_character.png"
        )
        print("✓ Character image created: outputs/workflow_character.png")
    except Exception as e:
        print(f"✗ Image generation error: {e}")
        print("  Continuing with workflow...")
    
    # =========================================================================
    # STEP 3: Generate Video Scene
    # =========================================================================
    print("\n[Step 3/4] Generating video scene...")
    print("-" * 80)
    
    video_gen = VideoGenerator(client)
    
    video_prompt = """A cinematic shot on Mars: An astronaut in a futuristic spacesuit 
    kneels in the red sand, carefully examining a glowing blue artifact. 
    The camera slowly dollies in, revealing wonder on their face visible through the helmet. 
    Dust particles float in the thin atmosphere, two moons visible in the pink sky, 
    dramatic sunset lighting, sci-fi movie aesthetic, ethereal mood."""
    
    try:
        video_result = video_gen.text_to_video(
            prompt=video_prompt,
            model="veo-3",
            duration=6,
            resolution="1080p",
            aspect_ratio="16:9",
            save_path="../outputs/workflow_scene.mp4",
            poll_interval=10,
            max_wait_time=600
        )
        print("✓ Video scene created: outputs/workflow_scene.mp4")
    except Exception as e:
        print(f"✗ Video generation error: {e}")
        print("  Continuing with workflow...")
    
    # =========================================================================
    # STEP 4: Create Audio Narration
    # =========================================================================
    print("\n[Step 4/4] Creating audio narration...")
    print("-" * 80)
    
    tts = TextToSpeech(client)
    
    narration = """Commander Sarah Chen had traveled 140 million miles to reach Mars, 
    but nothing could have prepared her for this moment. 
    The artifact pulsed with an otherworldly blue light, 
    its surface covered in symbols from a civilization that predated humanity itself. 
    As she lifted it from the crimson sand, a single thought echoed in her mind: 
    We are not alone."""
    
    try:
        audio_result = tts.generate(
            text=narration,
            model="tts-1-hd",
            voice="nova",
            speed=0.95,
            save_path="../outputs/workflow_narration.mp3"
        )
        print("✓ Audio narration created: outputs/workflow_narration.mp3")
    except Exception as e:
        print(f"✗ Audio generation error: {e}")
        print("  Continuing with workflow...")
    
    # =========================================================================
    # WORKFLOW COMPLETE
    # =========================================================================
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETE!")
    print("=" * 80)
    print("\nCreated files:")
    print("  📝 Story concept (displayed above)")
    print("  🎨 outputs/workflow_character.png (character image)")
    print("  🎬 outputs/workflow_scene.mp4 (video scene)")
    print("  🔊 outputs/workflow_narration.mp3 (audio narration)")
    print("\nYou now have all the elements for a multimedia story!")
    print("=" * 80 + "\n")


def workflow_marketing_campaign():
    """
    Workflow: Create a complete marketing campaign
    """
    print("\n" + "=" * 80)
    print("MARKETING CAMPAIGN WORKFLOW")
    print("Creating a complete marketing campaign for a product")
    print("=" * 80)
    
    client = ThucChienClient()
    
    # Step 1: Generate marketing copy
    print("\n[Step 1/3] Generating marketing copy...")
    text_gen = TextGenerator(client)
    
    copy_prompt = """Create marketing copy for a new eco-friendly water bottle:
    - Product name: "AquaPure"
    - Key features: Made from recycled materials, keeps drinks cold for 24 hours, leak-proof
    - Target audience: Environmentally conscious millennials
    - Include a catchy tagline and 2-3 sentences of description"""
    
    marketing_copy = text_gen.generate(
        prompt=copy_prompt,
        temperature=0.8,
        system_message="You are a creative marketing copywriter."
    )
    
    print(f"\nMarketing Copy:\n{marketing_copy}\n")
    
    # Step 2: Create product image
    print("\n[Step 2/3] Creating product visualization...")
    img_gen = ImageGenerator(client)
    
    product_prompt = """A sleek eco-friendly water bottle made from recycled materials,
    minimalist design, soft green and blue colors, on a clean white background
    with subtle nature elements like leaves, professional product photography,
    studio lighting, premium feel, 4K quality"""
    
    try:
        img_gen.text_to_image(
            prompt=product_prompt,
            model="dall-e-3",
            quality="hd",
            save_path="../outputs/workflow_product.png"
        )
        print("✓ Product image created")
    except Exception as e:
        print(f"✗ Image error: {e}")
    
    # Step 3: Create promotional video
    print("\n[Step 3/3] Creating promotional video...")
    video_gen = VideoGenerator(client)
    
    video_prompt = """Product showcase video: A beautiful eco-friendly water bottle 
    slowly rotating on a pedestal, soft green and blue colors, leaves falling gently 
    in the background, studio lighting with natural elements, clean and premium aesthetic,
    camera orbits smoothly around the product"""
    
    try:
        video_gen.text_to_video(
            prompt=video_prompt,
            duration=5,
            resolution="1080p",
            save_path="../outputs/workflow_promo.mp4"
        )
        print("✓ Promotional video created")
    except Exception as e:
        print(f"✗ Video error: {e}")
    
    print("\n" + "=" * 80)
    print("MARKETING CAMPAIGN COMPLETE!")
    print("=" * 80 + "\n")


def workflow_educational_content():
    """
    Workflow: Create educational content with explanations and visuals
    """
    print("\n" + "=" * 80)
    print("EDUCATIONAL CONTENT WORKFLOW")
    print("Creating educational content about solar system")
    print("=" * 80)
    
    client = ThucChienClient()
    
    # Step 1: Generate educational script
    print("\n[Step 1/3] Generating educational script...")
    text_gen = TextGenerator(client)
    
    conversation = text_gen.create_conversation(
        system_message="You are an engaging science educator."
    )
    
    lesson = conversation.send(
        "Create a brief, engaging explanation about Jupiter for middle school students. "
        "Include 3 interesting facts."
    )
    
    print(f"\nLesson Content:\n{lesson}\n")
    
    # Step 2: Create illustration
    print("\n[Step 2/3] Creating educational illustration...")
    img_gen = ImageGenerator(client)
    
    jupiter_prompt = """Educational illustration of Jupiter, showing the Great Red Spot,
    colorful bands of clouds, several of its moons in the background,
    clean educational style, clearly visible details, labeled features,
    suitable for a science textbook, space background with stars"""
    
    try:
        img_gen.text_to_image(
            prompt=jupiter_prompt,
            model="dall-e-3",
            save_path="../outputs/workflow_jupiter.png"
        )
        print("✓ Illustration created")
    except Exception as e:
        print(f"✗ Image error: {e}")
    
    # Step 3: Create narration
    print("\n[Step 3/3] Creating lesson narration...")
    tts = TextToSpeech(client)
    
    try:
        tts.generate(
            text=lesson,
            model="tts-1-hd",
            voice="echo",
            speed=0.9,
            save_path="../outputs/workflow_lesson.mp3"
        )
        print("✓ Narration created")
    except Exception as e:
        print(f"✗ Audio error: {e}")
    
    print("\n" + "=" * 80)
    print("EDUCATIONAL CONTENT COMPLETE!")
    print("=" * 80 + "\n")


def main():
    """Run workflow demos"""
    try:
        print("\n" + "=" * 80)
        print("ThucChien AI - Complete Workflow Demos")
        print("=" * 80)
        
        # Choose a workflow to run
        print("\nAvailable workflows:")
        print("1. Story Creation (story + character + scene + narration)")
        print("2. Marketing Campaign (copy + product image + promo video)")
        print("3. Educational Content (lesson + illustration + narration)")
        print("\nRunning Workflow 1: Story Creation")
        print("(Modify main() to run other workflows)")
        
        workflow_story_creation()
        
        # Uncomment to run other workflows:
        # workflow_marketing_campaign()
        # workflow_educational_content()
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.\n")
    except Exception as e:
        print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

