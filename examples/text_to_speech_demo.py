"""
Text-to-Speech Demo
Demonstrates various text-to-speech capabilities with different voices and use cases.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from thucchien_ai_sdk import ThucChienClient, TextToSpeech


def demo_simple_tts():
    """Demo: Simple text-to-speech"""
    print("\n" + "=" * 80)
    print("DEMO 1: Simple Text-to-Speech")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    text = "Hello! Welcome to the ThucChien AI text-to-speech demonstration."
    print(f"\nText: {text}")
    
    try:
        result = tts.generate(
            text=text,
            voice="alloy",
            save_path="../outputs/welcome.mp3"
        )
        print(f"\n✓ Audio generated successfully!")
        print(f"  Saved to: outputs/welcome.mp3")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_all_voices():
    """Demo: Compare all available voices"""
    print("\n" + "=" * 80)
    print("DEMO 2: All Available Voices")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    # Get voice information
    voices = TextToSpeech.get_available_voices()
    
    print("\nAvailable voices:")
    for voice in voices:
        print(f"  - {voice['name']}: {voice['description']}")
    
    text = "This is a sample of my voice. How do you like it?"
    print(f"\nGenerating samples with text: '{text}'")
    
    for voice in voices:
        try:
            result = tts.generate(
                text=text,
                voice=voice['name'],
                save_path=f"../outputs/voice_{voice['name']}.mp3"
            )
            print(f"  ✓ {voice['name']}: outputs/voice_{voice['name']}.mp3")
        except Exception as e:
            print(f"  ✗ {voice['name']}: Error - {e}")


def demo_audiobook_narration():
    """Demo: Audiobook-style narration"""
    print("\n" + "=" * 80)
    print("DEMO 3: Audiobook Narration")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    text = """
    Chapter One: The Discovery
    
    Dr. Sarah Chen had dedicated her entire career to the search for 
    extraterrestrial intelligence. Twenty years of analyzing radio signals, 
    examining data from deep space telescopes, and she had found nothing. 
    
    Until tonight.
    
    The pattern was unmistakable. A sequence of prime numbers, repeating 
    every thirty-seven minutes. It couldn't be natural. It couldn't be random. 
    Someone, or something, was trying to communicate.
    
    Her hands trembled as she reached for the phone to call her colleagues. 
    Everything was about to change.
    """
    
    print(f"\nGenerating audiobook narration...")
    print(f"Text length: {len(text)} characters")
    
    try:
        result = tts.generate(
            text=text,
            model="tts-1-hd",  # High quality for audiobook
            voice="fable",  # Expressive voice for storytelling
            speed=0.9,  # Slightly slower for comprehension
            save_path="../outputs/audiobook_chapter1.mp3"
        )
        print(f"\n✓ Audiobook narration created!")
        print(f"  Saved to: outputs/audiobook_chapter1.mp3")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_podcast_intro():
    """Demo: Podcast introduction"""
    print("\n" + "=" * 80)
    print("DEMO 4: Podcast Introduction")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    text = """
    Welcome to Tech Horizons, the podcast where we explore the cutting edge 
    of technology and innovation! I'm your host, and today we're diving deep 
    into the world of artificial intelligence and its impact on creative industries. 
    We'll be talking about the latest breakthroughs, ethical considerations, 
    and what the future might hold. So grab your headphones and let's get started!
    """
    
    print(f"\nGenerating podcast intro...")
    
    try:
        result = tts.generate(
            text=text,
            voice="nova",  # Energetic voice for podcast
            speed=1.05,  # Slightly faster for dynamic feel
            save_path="../outputs/podcast_intro.mp3"
        )
        print(f"\n✓ Podcast intro created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_tutorial_narration():
    """Demo: Tutorial step-by-step narration"""
    print("\n" + "=" * 80)
    print("DEMO 5: Tutorial Narration")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    tutorial_steps = [
        "Step 1: Open your web browser and navigate to the application homepage.",
        "Step 2: Click on the Sign In button located in the top right corner of the page.",
        "Step 3: Enter your email address and password in the provided fields.",
        "Step 4: Click the Submit button to complete the login process.",
        "Step 5: You're now logged in! You can access all features from the main dashboard.",
    ]
    
    print(f"\nGenerating {len(tutorial_steps)} tutorial steps...")
    
    try:
        results = tts.generate_multiple(
            texts=tutorial_steps,
            model="tts-1",
            voice="echo",  # Calm, clear voice for instructions
            speed=0.9,  # Slower for clarity
            output_dir="../outputs"
        )
        print(f"\n✓ Generated {len(results)} tutorial audio files!")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['file_path']}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_character_dialogue():
    """Demo: Different character voices"""
    print("\n" + "=" * 80)
    print("DEMO 6: Character Dialogue")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    dialogues = [
        ("I can't believe we actually found the treasure!", "nova", "character_a"),
        ("The map was right all along! Look at all this gold!", "shimmer", "character_b"),
        ("We need to be careful getting it out of here.", "onyx", "character_c"),
    ]
    
    print(f"\nGenerating dialogue for {len(dialogues)} characters...")
    
    for i, (text, voice, character) in enumerate(dialogues):
        print(f"\n{character.upper()} ({voice}): {text}")
        try:
            result = tts.generate(
                text=text,
                voice=voice,
                save_path=f"../outputs/dialogue_{i+1}_{character}.mp3"
            )
            print(f"  ✓ Generated")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def demo_announcement():
    """Demo: Public announcement style"""
    print("\n" + "=" * 80)
    print("DEMO 7: Public Announcement")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    text = """
    Attention all passengers. Flight 247 to San Francisco is now boarding at Gate 12. 
    Please have your boarding passes and identification ready. 
    We will begin boarding with passengers needing special assistance, 
    followed by first class, and then general boarding. Thank you for your patience.
    """
    
    print(f"\nGenerating announcement...")
    
    try:
        result = tts.generate(
            text=text,
            voice="onyx",  # Deep, authoritative voice
            speed=0.95,
            save_path="../outputs/announcement.mp3"
        )
        print(f"\n✓ Announcement created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_meditation_guide():
    """Demo: Meditation/relaxation guide"""
    print("\n" + "=" * 80)
    print("DEMO 8: Meditation Guide")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    text = """
    Find a comfortable position and gently close your eyes. 
    Take a deep breath in through your nose... and slowly exhale through your mouth. 
    Feel your body beginning to relax. Release any tension in your shoulders. 
    Let your thoughts drift away like clouds in the sky. 
    With each breath, you become more calm... more peaceful... more centered. 
    Stay here as long as you need.
    """
    
    print(f"\nGenerating meditation guide...")
    
    try:
        result = tts.generate(
            text=text,
            model="tts-1-hd",
            voice="shimmer",  # Soft, calming voice
            speed=0.8,  # Slow for relaxation
            save_path="../outputs/meditation.mp3"
        )
        print(f"\n✓ Meditation guide created!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def demo_different_speeds():
    """Demo: Different playback speeds"""
    print("\n" + "=" * 80)
    print("DEMO 9: Different Playback Speeds")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    text = "The quick brown fox jumps over the lazy dog."
    speeds = [0.5, 0.75, 1.0, 1.25, 1.5]
    
    print(f"\nText: {text}")
    print(f"Generating at different speeds: {speeds}")
    
    for speed in speeds:
        try:
            result = tts.generate(
                text=text,
                voice="alloy",
                speed=speed,
                save_path=f"../outputs/speed_{str(speed).replace('.', '_')}.mp3"
            )
            print(f"  ✓ Speed {speed}x: outputs/speed_{str(speed).replace('.', '_')}.mp3")
        except Exception as e:
            print(f"  ✗ Speed {speed}x: Error - {e}")


def demo_multilingual():
    """Demo: Multilingual text-to-speech"""
    print("\n" + "=" * 80)
    print("DEMO 10: Multilingual Support")
    print("=" * 80)
    
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    texts = [
        ("Hello, welcome to our service!", "english"),
        ("Bonjour, bienvenue dans notre service!", "french"),
        ("Hola, bienvenido a nuestro servicio!", "spanish"),
        ("Hallo, willkommen bei unserem Service!", "german"),
        ("Ciao, benvenuto al nostro servizio!", "italian"),
    ]
    
    print(f"\nGenerating greetings in {len(texts)} languages...")
    
    for text, language in texts:
        print(f"\n{language.capitalize()}: {text}")
        try:
            result = tts.generate(
                text=text,
                voice="alloy",
                save_path=f"../outputs/greeting_{language}.mp3"
            )
            print(f"  ✓ Generated")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def main():
    """Run all demos"""
    try:
        print("\n" + "=" * 80)
        print("ThucChien AI - Text-to-Speech Demos")
        print("=" * 80)
        
        # Run all demos
        demo_simple_tts()
        demo_all_voices()
        demo_audiobook_narration()
        demo_podcast_intro()
        demo_tutorial_narration()
        demo_character_dialogue()
        demo_announcement()
        demo_meditation_guide()
        demo_different_speeds()
        demo_multilingual()
        
        print("\n" + "=" * 80)
        print("All demos completed!")
        print("Check the outputs/ directory for generated audio files.")
        print("=" * 80 + "\n")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.\n")
    except Exception as e:
        print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

