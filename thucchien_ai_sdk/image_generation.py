"""
Image generation and editing module with multi-turn conversation support.
"""

import os
import base64
import requests
from typing import Optional, List, Dict, Union
import random
import json
import mimetypes

from .client import ThucChienClient


def save_images(image_data: bytes, save_path: str):
    """
    Save an image to a file.
    """
    with open(save_path, 'wb') as f:
        f.write(image_data)
    print(f"Image saved to: {save_path}")

def ensure_bytes_from_base64(base64_string: str) -> bytes:
    """
    Convert a base64 string to bytes.
    """
    if ',' in base64_string and base64_string.strip().startswith("data:"):
        header, encoded = base64_string.split(',', 1)
    else:
        encoded = base64_string
    return base64.b64decode(encoded)

def to_base64(image: Union[str, bytes]) -> (str, str):
    """
    Return a base64 string of the image (neither path nor bytes).
    """
    data = None
    mime_type = None
    if isinstance(image, str):
        with open(image, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            mime_type = mimetypes.guess_type(image)[0]
            if not mime_type:
                mime_type = "image/png"

    elif isinstance(image, (bytes, bytearray)):
        data = bytes(image)
        mime_type = "image/png"
    else:
        raise ValueError("Invalid image type")
    
    b64 = base64.b64encode(data).decode('utf-8')
    return b64, mime_type


class ImageGenerator:
    """
    Image generation and editing capabilities.
    Supports text-to-image, image-to-image (editing), and chat-based generation.
    """
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize ImageGenerator with a ThucChien.ai client.
        
        Args:
            client: ThucChienClient instance
        """
        self.client = client
        self.base_url = client.get_base_url()
        self.api_key = client.get_api_key()
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.timeout = 30
        
    def standard_generate_image(
        self,
        prompt: str,
        n: int = 1,
        image_size: str = "1k",
        aspect_ratio: str = "1:1",
        add_random_suffix: bool = True,
        save_path: Optional[str] = None,
    ) -> list[bytes]:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate
            n: Number of images to generate (1-4 for imagen-4)
            image_size: Image size (1k, 2k for imagen-4)
            aspect_ratio: Aspect ratio ("1:1", "3:4", "4:3", "9:16", and "16:9" for imagen 4)
            add_random_suffix: Whether to add a random suffix to the prompt for ignoring cached from api provider
            save_path: Optional path to save the image

        Returns:
            List of bytes of the generated images

        """
        
        data = {
            "model": "imagen-4",
            "prompt": prompt if not add_random_suffix else f"{prompt} [Random suffix: {random.randint(1, 1000)}]",
            "n": n,
            "imageSize": image_size,
            "aspectRatio": aspect_ratio,
        }
        
        url = f"{self.base_url}/images/generations"
        response = self._session.post(url, data=json.dumps(data), timeout=self.timeout)
        response.raise_for_status()
        
        result = response.json().get("data", [])

        saved = []

        if save_path:
            for i, item in enumerate(result, start=1):
                b64_image = item.get("b64_json")
                if b64_image:
                    image_data = ensure_bytes_from_base64(b64_image)
                    saved.append(image_data)
                    save_images(image_data, f"{save_path}_{i}.png")
                else:
                    print(f"Warning: No image data found for item {i}")        
        return saved


    def chat_generate_image(
        self,
        prompt: str,
        save_path: Optional[str] = None,
    ) -> bytes:
        """
        Generate an image using the chat completions endpoint.

        Args:
            prompt: Text description of the image to generate
            save_path: Optional path to save the generated image

        Returns:
            Bytes of the generated image
        """
        data = {
            "model": "gemini-2.5-flash-image-preview",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "modalities": ["text", "image"],
        }
        
        url = f"{self.base_url}/chat/completions"
        response = self._session.post(url, data=json.dumps(data), timeout=self.timeout)
        response.raise_for_status()
        
        result = response.json().get("choices", [])[0].get("message", {}).get("images", [])
        base64_url = result[0].get("image_url").get("url")
        image_data = ensure_bytes_from_base64(base64_url)
        
        if save_path:
            save_images(image_data, save_path)

        return image_data



class ImageEditor:
    """
    Image editing capabilities.
    Supports image-to-image (editing), image-to-image (editing), and chat-based generation.
    """
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize ImageEditor with a ThucChien.ai client.
        """
        self.client = client
        self.base_url = client.get_base_url()
        self.api_key = client.get_api_key()
        self.endpoint = "https://api.thucchien.ai/gemini/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
        self._session = requests.Session()
        self._session.headers.update({
            "x-google-api-key": self.api_key,
            "Content-Type": "application/json"
        })
        self.timeout = 30


    def edit_image(
        self,
        prompt: str,
        image: Union[str, bytes],
        aspect_ratio: Optional[str] = None,
        extra_generation_config: Optional[Dict] = None,
        save_path: Optional[str] = None,
    ) -> bytes:
        """
        Edit an image with a text prompt.

        Args:
            prompt: Text description of the image to edit
            image: Path to the input image or bytes of the image
            aspect_ratio: Aspect ratio (one of "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9" and "21:9")
            extra_generation_config: Optional extra generation config
            save_path: Optional path to save the edited image

        Returns:
            Bytes of the edited image
        """

        b64, mime_type = to_base64(image)
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": b64,
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {}
        }

        if aspect_ratio:
            data["generationConfig"]["imageConfig"] = {
                "aspectRatio": aspect_ratio,
            }
        
        if extra_generation_config:
            data["generationConfig"].update(extra_generation_config)
        
        response = self._session.post(self.endpoint, data=json.dumps(data), timeout=self.timeout)
        response.raise_for_status()

        result = response.json()

        inline = result["candidates"][0]["content"]["parts"][0]["inlineData"]
        out_b64 = inline["data"]
        image_data = ensure_bytes_from_base64(out_b64)

        if save_path:
            save_images(image_data, save_path)

        return image_data


