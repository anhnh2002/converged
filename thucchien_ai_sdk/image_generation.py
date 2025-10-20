"""
Image generation and editing module with multi-turn conversation support.
"""

import os
import base64
import requests
from typing import Optional, List, Dict
from datetime import datetime
from PIL import Image
from io import BytesIO
from .client import ThucChienClient


class ImageGenerator:
    """
    Image generation and editing capabilities.
    Supports text-to-image, image-to-image (editing), variations, and chat-based generation.
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
        
    def text_to_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        n: int = 1,
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "vivid",
        save_path: Optional[str] = None,
        response_format: str = "url",
    ) -> Dict:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image to generate
            model: Model to use (dall-e-2, dall-e-3)
            n: Number of images to generate (1-10 for dall-e-2, 1 for dall-e-3)
            size: Image size (256x256, 512x512, 1024x1024 for dall-e-2; 
                  1024x1024, 1792x1024, 1024x1792 for dall-e-3)
            quality: Image quality (standard or hd) - dall-e-3 only
            style: Style (vivid or natural) - dall-e-3 only
            save_path: Optional path to save the image
            response_format: "url" or "b64_json"
            
        Returns:
            Dictionary containing image URLs/data and metadata
        """
        url = f"{self.base_url}/images/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
        }
        
        # Add dall-e-3 specific parameters
        if model == "dall-e-3":
            data["quality"] = quality
            data["style"] = style
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Save images if path provided
        if save_path:
            self._save_images(result, save_path, response_format)
        
        return result
    
    def edit_image(
        self,
        image_path: str,
        prompt: str,
        mask_path: Optional[str] = None,
        model: str = "dall-e-2",
        n: int = 1,
        size: str = "1024x1024",
        save_path: Optional[str] = None,
        response_format: str = "url",
    ) -> Dict:
        """
        Edit an image based on a text prompt.
        
        Args:
            image_path: Path to the image to edit (must be PNG, < 4MB, square)
            prompt: Text description of the desired edit
            mask_path: Optional path to mask image (areas to edit should be transparent)
            model: Model to use (dall-e-2)
            n: Number of variations to generate (1-10)
            size: Image size (256x256, 512x512, 1024x1024)
            save_path: Optional path to save the edited image
            response_format: "url" or "b64_json"
            
        Returns:
            Dictionary containing edited image URLs/data
        """
        url = f"{self.base_url}/images/edits"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Prepare multipart form data
        files = {
            'image': open(image_path, 'rb'),
        }
        
        if mask_path:
            files['mask'] = open(mask_path, 'rb')
        
        data = {
            'prompt': prompt,
            'model': model,
            'n': n,
            'size': size,
            'response_format': response_format,
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Save images if path provided
        if save_path:
            self._save_images(result, save_path, response_format)
        
        return result
    
    def create_variation(
        self,
        image_path: str,
        model: str = "dall-e-2",
        n: int = 1,
        size: str = "1024x1024",
        save_path: Optional[str] = None,
        response_format: str = "url",
    ) -> Dict:
        """
        Create variations of an existing image.
        
        Args:
            image_path: Path to the image (must be PNG, < 4MB, square)
            model: Model to use (dall-e-2)
            n: Number of variations to generate (1-10)
            size: Image size (256x256, 512x512, 1024x1024)
            save_path: Optional path to save variations
            response_format: "url" or "b64_json"
            
        Returns:
            Dictionary containing variation URLs/data
        """
        url = f"{self.base_url}/images/variations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        files = {
            'image': open(image_path, 'rb'),
        }
        
        data = {
            'model': model,
            'n': n,
            'size': size,
            'response_format': response_format,
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Save images if path provided
        if save_path:
            self._save_images(result, save_path, response_format)
        
        return result
    
    def chat_generate_image(
        self,
        prompt: str,
        model: str = "gemini-2.5-flash-image-preview",
        save_path: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
    ) -> Dict:
        """
        Generate an image using the chat completions endpoint.
        This method uses multimodal chat models that can generate images directly in conversation.
        Returns base64-encoded image data.
        
        Args:
            prompt: Text description of the image to generate
            model: Model to use (gemini-2.5-flash-image-preview)
            save_path: Optional path to save the generated image
            messages: Optional list of previous messages for multi-turn generation
            
        Returns:
            Dictionary containing the chat response with image data
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Build messages
        if messages is None:
            messages = []
        
        # Add the current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        data = {
            "model": model,
            "messages": messages,
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract and save image if path provided
        if save_path:
            try:
                # Extract base64 image data from response
                base64_string = result['choices'][0]['message']['images'][0]['image_url']['url']
                
                # Remove data URI prefix if present
                if ',' in base64_string:
                    header, encoded = base64_string.split(',', 1)
                else:
                    encoded = base64_string
                
                # Decode and save
                image_data = base64.b64decode(encoded)
                
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"Image saved to: {save_path}")
                result['saved_path'] = save_path
                
            except (KeyError, IndexError) as e:
                print(f"Failed to parse image data from response: {e}")
        
        return result
    
    def create_editing_session(
        self,
        initial_image_path: Optional[str] = None,
        model: str = "dall-e-3",
    ) -> 'ImageEditingSession':
        """
        Create a multi-turn image editing session.
        
        Args:
            initial_image_path: Optional path to starting image
            model: Model to use
            
        Returns:
            ImageEditingSession instance
        """
        return ImageEditingSession(self, initial_image_path, model)
    
    def _save_images(self, result: Dict, save_path: str, response_format: str):
        """
        Helper method to save generated images.
        
        Args:
            result: API response containing image data
            save_path: Base path for saving images
            response_format: Format of the image data
        """
        for i, image_data in enumerate(result.get('data', [])):
            if response_format == "url":
                # Download from URL
                img_url = image_data.get('url')
                if img_url:
                    img_response = requests.get(img_url)
                    img = Image.open(BytesIO(img_response.content))
                    
                    # Generate filename
                    if len(result['data']) > 1:
                        path = save_path.replace('.png', f'_{i}.png')
                    else:
                        path = save_path
                    
                    img.save(path)
                    print(f"Image saved to: {path}")
            
            elif response_format == "b64_json":
                # Decode base64
                img_data = base64.b64decode(image_data.get('b64_json'))
                img = Image.open(BytesIO(img_data))
                
                # Generate filename
                if len(result['data']) > 1:
                    path = save_path.replace('.png', f'_{i}.png')
                else:
                    path = save_path
                
                img.save(path)
                print(f"Image saved to: {path}")


class ImageEditingSession:
    """
    Multi-turn image editing session with conversation history.
    """
    
    def __init__(
        self,
        image_generator: ImageGenerator,
        initial_image_path: Optional[str] = None,
        model: str = "dall-e-3",
    ):
        """
        Initialize an image editing session.
        
        Args:
            image_generator: ImageGenerator instance
            initial_image_path: Optional path to starting image
            model: Model to use
        """
        self.image_generator = image_generator
        self.model = model
        self.history: List[Dict] = []
        self.current_image_path = initial_image_path
        
        if initial_image_path:
            self.history.append({
                "action": "initial",
                "image_path": initial_image_path,
                "timestamp": datetime.now().isoformat(),
            })
    
    def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        save_path: Optional[str] = None,
    ) -> Dict:
        """
        Generate a new image in the session.
        
        Args:
            prompt: Text description
            size: Image size
            quality: Image quality
            save_path: Optional save path
            
        Returns:
            Generation result
        """
        if not save_path:
            save_path = f"outputs/session_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        result = self.image_generator.text_to_image(
            prompt=prompt,
            model=self.model,
            size=size,
            quality=quality,
            save_path=save_path,
        )
        
        self.current_image_path = save_path
        self.history.append({
            "action": "generate",
            "prompt": prompt,
            "image_path": save_path,
            "timestamp": datetime.now().isoformat(),
        })
        
        return result
    
    def edit(
        self,
        prompt: str,
        mask_path: Optional[str] = None,
        save_path: Optional[str] = None,
    ) -> Dict:
        """
        Edit the current image in the session.
        
        Args:
            prompt: Edit description
            mask_path: Optional mask path
            save_path: Optional save path
            
        Returns:
            Edit result
        """
        if not self.current_image_path:
            raise ValueError("No current image to edit. Generate or load an image first.")
        
        if not save_path:
            save_path = f"outputs/session_edit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        result = self.image_generator.edit_image(
            image_path=self.current_image_path,
            prompt=prompt,
            mask_path=mask_path,
            model="dall-e-2",  # Only dall-e-2 supports editing
            save_path=save_path,
        )
        
        self.current_image_path = save_path
        self.history.append({
            "action": "edit",
            "prompt": prompt,
            "mask_path": mask_path,
            "image_path": save_path,
            "timestamp": datetime.now().isoformat(),
        })
        
        return result
    
    def get_history(self) -> List[Dict]:
        """Get the editing session history."""
        return self.history.copy()
    
    def get_current_image(self) -> Optional[str]:
        """Get the path to the current image."""
        return self.current_image_path
    
    def __repr__(self):
        return f"ImageEditingSession(model='{self.model}', edits={len(self.history)})"


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_chat_generate_image(client: ThucChienClient):
    """Example: Generate an image using chat endpoint (Gemini)"""
    generator = ImageGenerator(client)
    
    prompt = """A futuristic cityscape at sunset, with flying cars and neon lights. 
    High resolution, photorealistic, 8k"""
    
    result = generator.chat_generate_image(
        prompt=prompt,
        model="gemini-2.5-flash-image-preview",
        save_path="outputs/chat_generated_city.png",
    )
    
    print("Image generated via chat endpoint!")
    print(f"Model used: {result.get('model', 'N/A')}")
    
    return result


def example_text_to_image(client: ThucChienClient):
    """Example: Generate an image from text"""
    generator = ImageGenerator(client)
    
    prompt = """A serene Japanese garden with a koi pond, cherry blossom trees in full bloom, 
    a traditional wooden bridge over the water, and Mount Fuji visible in the background 
    during sunset. Photorealistic style."""
    
    result = generator.text_to_image(
        prompt=prompt,
        model="dall-e-3",
        size="1024x1024",
        quality="hd",
        style="vivid",
        save_path="outputs/japanese_garden.png",
    )
    
    print("Image generated successfully!")
    print(f"Revised prompt: {result['data'][0].get('revised_prompt', 'N/A')}")
    
    return result


def example_image_editing(client: ThucChienClient):
    """Example: Edit an existing image"""
    generator = ImageGenerator(client)
    
    result = generator.edit_image(
        image_path="outputs/landscape.png",
        prompt="Add a red hot air balloon floating in the sky",
        model="dall-e-2",
        size="1024x1024",
        save_path="outputs/landscape_with_balloon.png",
    )
    
    print("Image edited successfully!")
    return result


def example_image_variations(client: ThucChienClient):
    """Example: Create variations of an image"""
    generator = ImageGenerator(client)
    
    result = generator.create_variation(
        image_path="outputs/portrait.png",
        n=3,
        size="1024x1024",
        save_path="outputs/portrait_variation.png",
    )
    
    print("Image variations created successfully!")
    return result


def example_multi_turn_editing(client: ThucChienClient):
    """Example: Multi-turn image editing session"""
    generator = ImageGenerator(client)
    
    # Create an editing session
    session = generator.create_editing_session(model="dall-e-3")
    
    # First: Generate initial image
    print("Step 1: Generating initial image...")
    session.generate(
        prompt="A modern minimalist living room with large windows",
        save_path="outputs/session_step1.png",
    )
    
    # Second: Edit to add furniture (would use dall-e-2 for editing)
    print("Step 2: Adding furniture...")
    # Note: This would require converting to PNG and using dall-e-2
    # For demonstration, we'll generate a new image with the addition
    session.generate(
        prompt="A modern minimalist living room with large windows, now with a grey sectional sofa and coffee table",
        save_path="outputs/session_step2.png",
    )
    
    # Third: Further refinement
    print("Step 3: Adding plants...")
    session.generate(
        prompt="A modern minimalist living room with large windows, grey sectional sofa, coffee table, and several potted plants",
        save_path="outputs/session_step3.png",
    )
    
    # Get history
    history = session.get_history()
    print(f"\nEditing session complete! Total steps: {len(history)}")
    print(f"Final image: {session.get_current_image()}")
    
    return history


def example_detailed_prompt(client: ThucChienClient):
    """Example: Detailed prompt with style specifications"""
    generator = ImageGenerator(client)
    
    prompt = """
    A cyberpunk street scene at night in Neo-Tokyo:
    - Neon signs in Japanese and English reflecting on wet pavement
    - A figure in a long coat walking through the rain
    - Holographic advertisements floating in the air
    - Flying cars in the background
    - Atmospheric fog and volumetric lighting
    - Blade Runner aesthetic with vibrant purples, blues, and magentas
    - Highly detailed, cinematic composition, 8K quality
    """
    
    result = generator.text_to_image(
        prompt=prompt,
        model="dall-e-3",
        size="1792x1024",  # Wide format for cinematic feel
        quality="hd",
        style="vivid",
        save_path="outputs/cyberpunk_street.png",
    )
    
    print("Cyberpunk scene generated!")
    return result


def example_multiple_variations(client: ThucChienClient):
    """Example: Generate multiple images from one prompt"""
    generator = ImageGenerator(client)
    
    prompt = "A cute robot mascot character, friendly and approachable, suitable for a tech company"
    
    result = generator.text_to_image(
        prompt=prompt,
        model="dall-e-2",  # dall-e-2 supports multiple images
        n=4,
        size="512x512",
        save_path="outputs/robot_mascot.png",
    )
    
    print(f"Generated {len(result['data'])} robot mascot variations!")
    return result


# =============================================================================
# BEST PRACTICES AND TIPS
# =============================================================================

"""
IMAGE GENERATION BEST PRACTICES:

1. Chat-based Image Generation (Gemini):
   - Uses chat/completions endpoint with gemini-2.5-flash-image-preview model
   - Returns base64-encoded images in the chat response
   - Supports multi-turn conversations for iterative image refinement
   - Good for conversational image generation workflows
   - Images are returned inline, not via URL

2. Text-to-Image Prompting:
   - Be specific and descriptive
   - Include style keywords: "photorealistic", "oil painting", "digital art"
   - Specify lighting: "golden hour", "studio lighting", "dramatic shadows"
   - Mention composition: "centered", "rule of thirds", "wide angle"
   - Add quality keywords: "highly detailed", "4K", "professional"

3. Image Editing:
   - Clearly describe what to change
   - Use phrases like "add", "remove", "replace", "transform"
   - Specify how the edit should blend with the original
   - Consider creating a mask for precise edits

4. Model Selection:
   - Gemini 2.5 Flash Image: Chat-based, conversational, base64 response
   - DALL-E 3: Better quality, more prompt adherence, single image only
   - DALL-E 2: Supports multiple images, editing, and variations

5. Size Recommendations:
   - Square (1024x1024): General purpose, portraits
   - Wide (1792x1024): Landscapes, cinematic shots
   - Tall (1024x1792): Portraits, vertical compositions

6. Quality vs Speed:
   - "standard": Faster, good quality
   - "hd": Slower, exceptional detail

7. Style Options (DALL-E 3):
   - "vivid": Hyper-real, dramatic images
   - "natural": More natural, less dramatic

8. Common Issues:
   - Images must be PNG format for editing
   - Images must be square for editing
   - Image size must be < 4MB
   - For best editing results, create a proper mask
"""


if __name__ == "__main__":
    try:
        client = ThucChienClient()
        
        print("=" * 80)
        print("Example: Text-to-Image Generation")
        print("=" * 80)
        example_text_to_image(client)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.")
    except Exception as e:
        print(f"Error: {e}")

