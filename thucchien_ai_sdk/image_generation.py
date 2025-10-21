"""
Image generation and editing module with multi-turn conversation support.
"""

import requests
from typing import Optional, List, Dict, Union
import random
import json

from .client import ThucChienClient
from .utils import save_images, ensure_bytes_from_base64, to_base64


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


if __name__ == "__main__":

    client = ThucChienClient()
    image_gen = ImageGenerator(client)
    image_editor = ImageEditor(client)

    # Example 3: Image editing (requires an existing image)
    print("\n3️⃣  Image Editing")
    print("-" * 60)
    
    # First, check if we have an image to edit
    import os
    if os.path.exists("outputs/standard_image_1.png"):
        edit_prompt = "Add a small boat on the lake"
        print(f"Edit prompt: {edit_prompt}")
        
        edited_image = image_editor.edit_image(
            prompt=edit_prompt,
            image="outputs/standard_image_1.png",
            aspect_ratio="16:9",
            save_path="outputs/edited_image.png"
        )
        print("✅ Image edited successfully")
    else:
        print("⚠️  No image found to edit. Run standard generation first.")