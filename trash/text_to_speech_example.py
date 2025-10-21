#!/usr/bin/env python3
"""
Simple example for text-to-speech using ThucChien.ai SDK.

This demonstrates:
1. Converting text to speech with different voices
2. Saving audio files
"""

import os
from thucchien_ai_sdk import ThucChienClient, TextToSpeech


def main():
    # Initialize client
    client = ThucChienClient()
    tts = TextToSpeech(client)
    
    # Create output directory
    os.makedirs("outputs", exist_ok=True)
    
    print("=" * 60)
    print("TEXT-TO-SPEECH EXAMPLES")
    print("=" * 60)
    
    # Example 1: Male voice
    print("\n1️⃣  Generating speech with male voice (Puck)")
    print("-" * 60)
    text_male = "Hello! This is a demonstration of text to speech with a male voice. The technology is quite impressive!"
    print(f"Text: {text_male}")
    
    success = tts.generate(
        text=text_male,
        model="gemini-2.5-flash-preview-tts",
        voice="Puck",
        save_path="outputs/speech_male.mp3"
    )
    
    if success:
        print("✅ Male voice audio generated")
    else:
        print("❌ Failed to generate male voice audio")
    
    # Example 2: Female voice
    print("\n2️⃣  Generating speech with female voice (Aoede)")
    print("-" * 60)
    text_female = "Welcome to ThucChien AI! This is an example of a female voice using the text to speech API."
    print(f"Text: {text_female}")
    
    success = tts.generate(
        text=text_female,
        model="gemini-2.5-flash-preview-tts",
        voice="Aoede",
        save_path="outputs/speech_female.mp3"
    )
    
    if success:
        print("✅ Female voice audio generated")
    else:
        print("❌ Failed to generate female voice audio")
    
    # Example 3: Longer text
    print("\n3️⃣  Generating speech from longer text")
    print("-" * 60)
    long_text = """
    Artificial intelligence is transforming the way we interact with technology.
    From natural language processing to computer vision, AI systems are becoming
    increasingly sophisticated. Text-to-speech is one of these amazing capabilities,
    allowing us to convert written text into natural sounding speech.
    """
    print(f"Text: {long_text[:100]}...")
    
    success = tts.generate(
        text=long_text,
        model="gemini-2.5-flash-preview-tts",
        voice="Puck",
        save_path="outputs/speech_long.mp3"
    )
    
    if success:
        print("✅ Long text audio generated")
    else:
        print("❌ Failed to generate long text audio")
    
    print("\n" + "=" * 60)
    print("✨ All examples completed!")
    print(f"📁 Check the 'outputs' folder for generated audio files")
    print("=" * 60)


if __name__ == "__main__":
    main()

