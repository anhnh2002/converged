"""
Text-to-speech module for audio generation.
"""

import requests
from typing import Optional, Dict, List
from datetime import datetime
from .client import ThucChienClient


class TextToSpeech:
    """
    Text-to-speech capabilities for converting text to audio.
    """
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize TextToSpeech with a ThucChien.ai client.
        
        Args:
            client: ThucChienClient instance
        """
        self.client = client
        self.base_url = client.get_base_url()
        self.api_key = client.get_api_key()
    
    def generate(
        self,
        text: str,
        model: str = "tts-1",
        voice: str = "alloy",
        response_format: str = "mp3",
        speed: float = 1.0,
        save_path: Optional[str] = None,
    ) -> Dict:
        """
        Convert text to speech.
        
        Args:
            text: The text to convert to speech (max 4096 characters)
            model: Model to use (tts-1 or tts-1-hd)
                   - tts-1: Standard quality, faster
                   - tts-1-hd: Higher quality, slower
            voice: Voice to use. Available voices:
                   - alloy: Neutral, balanced
                   - echo: Male, calm
                   - fable: British accent, expressive
                   - onyx: Deep male voice
                   - nova: Female, energetic
                   - shimmer: Female, soft
            response_format: Audio format (mp3, opus, aac, flac, wav, pcm)
            speed: Playback speed (0.25 to 4.0)
            save_path: Optional path to save the audio file
            
        Returns:
            Dictionary with audio URL/data and metadata
        """
        url = f"{self.base_url}/audio/speech"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "input": text,
            "voice": voice,
            "response_format": response_format,
            "speed": speed,
        }
        
        print(f"Generating speech for text: {text[:100]}...")
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Save audio if path provided
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved to: {save_path}")
            
            return {
                "file_path": save_path,
                "format": response_format,
                "model": model,
                "voice": voice,
            }
        else:
            # Return audio data
            return {
                "audio_data": response.content,
                "format": response_format,
                "model": model,
                "voice": voice,
            }
    
    def generate_from_file(
        self,
        file_path: str,
        model: str = "tts-1",
        voice: str = "alloy",
        response_format: str = "mp3",
        speed: float = 1.0,
        save_path: Optional[str] = None,
    ) -> Dict:
        """
        Convert text from a file to speech.
        
        Args:
            file_path: Path to text file to read
            model: Model to use
            voice: Voice to use
            response_format: Audio format
            speed: Playback speed
            save_path: Optional path to save audio
            
        Returns:
            Dictionary with audio URL/data and metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.generate(
            text=text,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            save_path=save_path,
        )
    
    def generate_multiple(
        self,
        texts: List[str],
        model: str = "tts-1",
        voice: str = "alloy",
        response_format: str = "mp3",
        speed: float = 1.0,
        output_dir: str = "outputs",
    ) -> List[Dict]:
        """
        Convert multiple texts to speech.
        
        Args:
            texts: List of texts to convert
            model: Model to use
            voice: Voice to use
            response_format: Audio format
            speed: Playback speed
            output_dir: Directory to save audio files
            
        Returns:
            List of dictionaries with results for each text
        """
        results = []
        
        for i, text in enumerate(texts):
            save_path = f"{output_dir}/speech_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{response_format}"
            
            result = self.generate(
                text=text,
                model=model,
                voice=voice,
                response_format=response_format,
                speed=speed,
                save_path=save_path,
            )
            
            results.append(result)
        
        return results
    
    @staticmethod
    def get_available_voices() -> List[Dict[str, str]]:
        """
        Get list of available voices with descriptions.
        
        Returns:
            List of voice information dictionaries
        """
        return [
            {
                "name": "alloy",
                "description": "Neutral and balanced voice, suitable for general use",
                "gender": "neutral",
            },
            {
                "name": "echo",
                "description": "Male voice, calm and measured",
                "gender": "male",
            },
            {
                "name": "fable",
                "description": "British accent, expressive and engaging",
                "gender": "neutral",
            },
            {
                "name": "onyx",
                "description": "Deep male voice, authoritative",
                "gender": "male",
            },
            {
                "name": "nova",
                "description": "Female voice, energetic and bright",
                "gender": "female",
            },
            {
                "name": "shimmer",
                "description": "Female voice, soft and gentle",
                "gender": "female",
            },
        ]


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_simple_tts(client: ThucChienClient):
    """Example: Simple text-to-speech"""
    tts = TextToSpeech(client)
    
    text = "Hello! Welcome to the ThucChien AI text-to-speech service. This is a demonstration of our voice synthesis capabilities."
    
    result = tts.generate(
        text=text,
        voice="alloy",
        save_path="outputs/welcome_speech.mp3",
    )
    
    print("Speech generated successfully!")
    return result


def example_different_voices(client: ThucChienClient):
    """Example: Generate same text with different voices"""
    tts = TextToSpeech(client)
    
    text = "This is a sample of the voice. How do you like it?"
    voices = ["alloy", "echo", "nova", "shimmer"]
    
    for voice in voices:
        result = tts.generate(
            text=text,
            voice=voice,
            save_path=f"outputs/voice_sample_{voice}.mp3",
        )
        print(f"Generated with {voice} voice")
    
    print("All voice samples generated!")


def example_audiobook(client: ThucChienClient):
    """Example: Generate audiobook-style narration"""
    tts = TextToSpeech(client)
    
    text = """
    Chapter One: The Beginning
    
    It was a dark and stormy night. The rain poured down in sheets, 
    drumming against the windows of the old mansion on the hill. 
    Inside, a single candle flickered in the library, casting dancing 
    shadows across the leather-bound books that lined the walls.
    
    Dr. Eleanor Hart sat at her desk, poring over an ancient manuscript 
    she had discovered in the archives. The text was in a language she 
    had never seen before, yet somehow, she could understand it.
    """
    
    result = tts.generate(
        text=text,
        model="tts-1-hd",  # High quality for audiobook
        voice="fable",  # Expressive voice for storytelling
        speed=0.9,  # Slightly slower for better comprehension
        save_path="outputs/audiobook_chapter1.mp3",
    )
    
    print("Audiobook chapter generated!")
    return result


def example_podcast_intro(client: ThucChienClient):
    """Example: Generate podcast introduction"""
    tts = TextToSpeech(client)
    
    text = """
    Welcome to Tech Talk, the podcast where we explore the latest in 
    technology and innovation. I'm your host, and today we're diving 
    into the world of artificial intelligence and its impact on creative 
    industries. Let's get started!
    """
    
    result = tts.generate(
        text=text,
        voice="nova",  # Energetic voice for podcast
        speed=1.1,  # Slightly faster for dynamic feel
        save_path="outputs/podcast_intro.mp3",
    )
    
    print("Podcast intro generated!")
    return result


def example_multilingual_support(client: ThucChienClient):
    """Example: Generate speech in different languages"""
    tts = TextToSpeech(client)
    
    texts = [
        ("Hello, how are you today?", "english"),
        ("Bonjour, comment allez-vous aujourd'hui?", "french"),
        ("Hola, ¿cómo estás hoy?", "spanish"),
        ("Guten Tag, wie geht es Ihnen heute?", "german"),
    ]
    
    for text, language in texts:
        result = tts.generate(
            text=text,
            voice="alloy",
            save_path=f"outputs/greeting_{language}.mp3",
        )
        print(f"Generated {language} greeting")
    
    print("Multilingual greetings generated!")


def example_voice_comparison(client: ThucChienClient):
    """Example: Compare all available voices"""
    tts = TextToSpeech(client)
    
    # Get voice information
    voices = TextToSpeech.get_available_voices()
    
    print("Available Voices:")
    print("=" * 80)
    for voice in voices:
        print(f"Name: {voice['name']}")
        print(f"Description: {voice['description']}")
        print(f"Gender: {voice['gender']}")
        print("-" * 80)
    
    # Generate sample with each voice
    text = "This is a comparison of the available voices in the text-to-speech system."
    
    for voice in voices:
        result = tts.generate(
            text=text,
            voice=voice['name'],
            save_path=f"outputs/comparison_{voice['name']}.mp3",
        )
        print(f"Generated sample with {voice['name']}")


def example_tutorial_narration(client: ThucChienClient):
    """Example: Generate tutorial narration"""
    tts = TextToSpeech(client)
    
    tutorial_steps = [
        "Step 1: Open your web browser and navigate to the application.",
        "Step 2: Click on the 'Sign In' button in the top right corner.",
        "Step 3: Enter your email address and password, then click 'Submit'.",
        "Step 4: You're now logged in! Let's explore the main features.",
        "Step 5: Navigate to the dashboard to see your personalized content.",
    ]
    
    results = tts.generate_multiple(
        texts=tutorial_steps,
        model="tts-1",
        voice="echo",  # Calm voice for instructions
        speed=0.95,  # Slightly slower for clarity
        output_dir="outputs",
    )
    
    print(f"Generated {len(results)} tutorial narration files!")
    return results


def example_character_dialogue(client: ThucChienClient):
    """Example: Generate dialogue for different characters"""
    tts = TextToSpeech(client)
    
    dialogues = [
        ("I can't believe we finally made it to the summit!", "nova"),
        ("The view from up here is absolutely breathtaking.", "shimmer"),
        ("We should start heading back before it gets dark.", "onyx"),
    ]
    
    for i, (text, voice) in enumerate(dialogues):
        result = tts.generate(
            text=text,
            voice=voice,
            save_path=f"outputs/dialogue_{i+1}_{voice}.mp3",
        )
        print(f"Generated dialogue {i+1} with {voice} voice")
    
    print("Character dialogue generated!")


# =============================================================================
# BEST PRACTICES AND TIPS
# =============================================================================

"""
TEXT-TO-SPEECH BEST PRACTICES:

1. Voice Selection:
   - Alloy: General purpose, neutral tone
   - Echo: Male voice, calm and professional
   - Fable: Storytelling, expressive
   - Onyx: Deep voice, authoritative
   - Nova: Energetic, upbeat content
   - Shimmer: Soft, gentle, soothing

2. Model Selection:
   - tts-1: Standard quality, faster, cheaper
   - tts-1-hd: Higher quality, better for:
     * Audiobooks
     * Professional content
     * Critical listening applications

3. Speed Recommendations:
   - 0.25-0.75: Very slow (accessibility)
   - 0.75-0.95: Slow (learning, instructions)
   - 1.0: Normal speed
   - 1.05-1.25: Fast (energetic content)
   - 1.25-4.0: Very fast (time-lapse effect)

4. Text Formatting Tips:
   - Use punctuation for natural pauses
   - Add commas for breath points
   - Use periods for longer pauses
   - Exclamation marks for emphasis
   - Question marks for rising intonation

5. Format Selection:
   - mp3: Good compression, universal support
   - opus: Best for real-time streaming
   - aac: Good quality, Apple ecosystems
   - flac: Lossless, large files
   - wav: Uncompressed, editing
   - pcm: Raw audio data

6. Character Limits:
   - Maximum: 4096 characters per request
   - For longer texts, split into chunks
   - Use generate_multiple() for batches

7. Use Cases:
   - Audiobooks: tts-1-hd, fable/echo, speed 0.9
   - Podcasts: tts-1, nova/echo, speed 1.0-1.1
   - Tutorials: tts-1, echo/alloy, speed 0.95
   - Announcements: tts-1, onyx/nova, speed 1.0
   - Meditation: tts-1-hd, shimmer, speed 0.8

8. Quality Tips:
   - Use proper grammar and spelling
   - Add SSML-style pauses with punctuation
   - Break long sentences into shorter ones
   - Avoid special characters and symbols
   - Use phonetic spelling for difficult words

9. Cost Optimization:
   - Use tts-1 for development/testing
   - Switch to tts-1-hd for production
   - Batch similar requests together
   - Cache frequently used audio

10. Common Issues:
    - Mispronounced words: Try alternate spelling
    - Unnatural pauses: Adjust punctuation
    - Too fast/slow: Adjust speed parameter
    - Wrong emphasis: Rephrase sentence structure
"""


if __name__ == "__main__":
    try:
        client = ThucChienClient()
        
        print("=" * 80)
        print("Example: Simple Text-to-Speech")
        print("=" * 80)
        example_simple_tts(client)
        
        print("\n" + "=" * 80)
        print("Example: Voice Comparison")
        print("=" * 80)
        example_voice_comparison(client)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.")
    except Exception as e:
        print(f"Error: {e}")

