"""
Image generation and editing module with multi-turn conversation support.
"""

import requests
from typing import Optional, List, Dict, Union, Any
import random
import json

from .client import ThucChienClient
from .utils import save_images, ensure_bytes_from_base64, to_base64


class StandardImageGenerator:
    """
    Image generation capabilities.
    Supports text-to-image generation.
    Especially useful for generating standalone images without needs of consistency
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
        aspect_ratio: str = "1:1",
        add_random_suffix: bool = True,
        save_path: Optional[str] = None,
    ) -> list[bytes]:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate
            n: Number of images to generate (1-4 for imagen-4)
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
                    if n > 1:
                        save_images(image_data, f"{i}_{save_path}")
                    else:
                        save_images(image_data, save_path)
                else:
                    print(f"Warning: No image data found for item {i}")        
        return saved



class ConversationalImageGenerator:
    """
    Conversation-based image generation capabilities.
    Supports conversation-based image generation with multi-turn conversation support.
    Especially useful for generating list of images with consistent style, content, object, human, etc. in order to make a storyboard, comic, etc.
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
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        })
        self.timeout = 30

    def generate(
        self,
        prompt: str,
        prev_contents: List[Dict[str, Any]] = [],
        aspect_ratio: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> (str, str):
        """
        Generate a new image from a text prompt.
        
        Args:
            prompt (str): Text description of the image to generate
            prev_contents (List[Dict[str, Any]], optional): List of history contents for providing context and history of the conversation to generate the image consistently with previous images
                - contents format:  [
                                        {
                                            'role': 'user'/'model',
                                            'parts':    [
                                                            {'text': 'text'},
                                                            {'inlineData': {'mime_type': '<mime_type>', 'data': '<base64_data>'}},
                                                            ...
                                                        ]
                                        },
                                        ...
                                    ]
            aspect_ratio (str): Aspect ratio of the generated image. Options:
                - Landscape: "21:9", "16:9", "4:3", "3:2"
                - Square: "1:1"
                - Portrait: "9:16", "3:4", "2:3"
                - Flexible: "5:4", "4:5"
            save_path (str, optional): Path to save the generated image
            
        Returns:
            (generated_image_base64, generated_image_mime_type)


        Example Usage:
            - Use case 1: Generate a single image with a text prompt:
                ```python
                image_gen.generate(
                    prompt="A serene mountain landscape at sunset with a lake reflecting the sky",
                    aspect_ratio="16:9",
                    save_path="outputs/moutain_landscape.png"
                )
                ```
            - Use case 2:Edit an existing image:
                ```python
                image_gen.generate(
                    prompt="Add a small boat on the lake",
                    prev_contents=[
                        {"role": "user", "parts": [{"inlineData": {"mime_type": "<mime_type_of_the_existing_image>", "data": "<base64_data_of_the_existing_image>"}}]},
                    ],
                    aspect_ratio="16:9",
                    save_path="outputs/moutain_landscape_with_boat.png"
                )
                ```
            - Use case 3: Generate a list of images with consistent object (MC) for a news report storyboard:
                ```python
                # image 1: Reporter portrait
                reporter_portrait_prompt = "A close-up portrait of the reporter standing in front of a newsroom backdrop. Add an on-screen lower-third text: “Maria Chen — Senior Field Correspondent, Global News.” She wears a professional outfit (navy blazer, press badge, holding microphone with network logo). Calm and confident expression, ready to report."
                reporter_portrait_mime_type, reporter_portrait_base64 = image_gen.generate(
                    prompt=reporter_portrait_prompt,
                    aspect_ratio="16:9",
                    save_path="outputs/reporter_portrait.png"
                )

                # image 2: Reporter sitting at the anchor desk
                reporter_sitting_prompt = "The reporter sits at the anchor desk in a modern TV studio. Multiple display screens show world maps and headlines. Bright, professional lighting and sleek digital graphics in the background."
                reporter_sitting_mime_type, reporter_sitting_base64 = image_gen.generate(
                    prompt=reporter_sitting_prompt,
                    prev_contents=[
                        {"role": "user", "parts": [{"text": reporter_portrait_prompt}]},
                        {"role": "model", "parts": [{"inlineData": {"mime_type": reporter_portrait_mime_type, "data": reporter_portrait_base64}}]},
                    ],
                    aspect_ratio="16:9",
                    save_path="outputs/reporter_sitting.png"
                )
                # image 3: Reporter reacting to urgent breaking news
                reporter_breaking_news_prompt = "The same reporter reacts to urgent breaking news. Red “BREAKING NEWS” graphics flash behind her as she looks at a monitor, microphone on desk. Serious, focused demeanor."
                reporter_breaking_news_mime_type, reporter_breaking_news_base64 = image_gen.generate(
                    prompt=reporter_breaking_news_prompt,
                    prev_contents=[
                        {"role": "user", "parts": [{"text": reporter_portrait_prompt}]},
                        {"role": "model", "parts": [{"inlineData": {"mime_type": reporter_portrait_mime_type, "data": reporter_portrait_base64}}]},
                        {"role": "user", "parts": [{"text": reporter_sitting_prompt}]},
                        {"role": "model", "parts": [{"inlineData": {"mime_type": reporter_sitting_mime_type, "data": reporter_sitting_base64}}]},
                    ],
                    aspect_ratio="16:9",
                    save_path="outputs/reporter_breaking_news.png"
                )

                ...
                ```
        """

        payload = {
            "contents": [
                *prev_contents,
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
        }

        if aspect_ratio:
            payload["generationConfig"] = {
                "imageConfig": {
                    "aspectRatio": aspect_ratio
                }
            }
        
        response = self._session.post(self.endpoint, data=json.dumps(payload), timeout=self.timeout)
        response.raise_for_status()

        result = response.json()

        inline = None
        for part in result["candidates"][0]["content"]["parts"]:
            if "inlineData" in part:
                inline = part["inlineData"]
                break
            elif "text" in part:
                print(f"text: {part['text']}")

        if not inline:
            raise ValueError("No inline data found in the response")

        out_b64 = inline["data"]
        out_mime_type = inline["mimeType"]
        image_data = ensure_bytes_from_base64(out_b64)

        if save_path:
            save_images(image_data, save_path)

        return out_b64, out_mime_type
