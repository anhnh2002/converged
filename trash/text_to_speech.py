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
        self.base_url = "https://api.thucchien.ai/audio/speech"
        self.api_key = client.get_api_key()
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.timeout = 30
    
    def generate(
        self,
        text: str,
        model: str = "gemini-2.5-flash-preview-tts",
        voice: str = "Puck",
        save_path: Optional[str] = None,
    ) -> bool:
        """
        Convert text to speech.
        
        Args:
            text: The text to convert to speech (max 4096 characters)
            prompt: Optional prompt to use for the speech generation
            model: Model to use (gemini-2.5-flash-preview-tts, gemini-2.5-pro-preview-tts)
            voice: Puck (male), Aoede (female)
            save_path: Optional path to save the audio file
            
        Returns:
            True if successful, False otherwise
        """
        data = {
            "model": model,
            "input": text,
            "voice": voice,
        }
        
        print(f"Generating speech for text: {text[:20]}...")
        
        response = requests.post(self.base_url, headers=self._session.headers, json=data, stream=True)
        response.raise_for_status()
        
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Audio saved to: {save_path}")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
