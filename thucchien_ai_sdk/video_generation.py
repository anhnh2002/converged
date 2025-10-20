"""
Video generation module with support for text-to-video and image-to-video.
"""

import requests
import time
from typing import Optional, Dict
from datetime import datetime
from .client import ThucChienClient


class VideoGenerator:
    """
    Video generation capabilities.
    Supports text-to-video and image-to-video generation.
    """
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize VideoGenerator with a ThucChien.ai client.
        
        Args:
            client: ThucChienClient instance
        """
        self.client = client
        self.base_url = client.get_base_url()
        self.api_key = client.get_api_key()
    
    def text_to_video(
        self,
        prompt: str,
        model: str = "veo-3",
        duration: int = 5,
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        fps: int = 24,
        save_path: Optional[str] = None,
        poll_interval: int = 10,
        max_wait_time: int = 600,
    ) -> Dict:
        """
        Generate a video from a text prompt.
        
        Args:
            prompt: Text description of the video to generate
            model: Model to use (veo-3, veo-2, runway, etc.)
            duration: Video duration in seconds
            resolution: Video resolution (720p, 1080p, 4k)
            aspect_ratio: Aspect ratio (16:9, 9:16, 1:1)
            fps: Frames per second (24, 30, 60)
            save_path: Optional path to save the video
            poll_interval: Seconds between status checks
            max_wait_time: Maximum time to wait for generation (seconds)
            
        Returns:
            Dictionary with video URL and metadata
        """
        url = f"{self.base_url}/videos/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "fps": fps,
        }
        
        print(f"Starting video generation with prompt: {prompt[:100]}...")
        
        # Submit generation request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        job_id = result.get("id")
        
        if not job_id:
            print("Warning: No job ID returned, returning result as-is")
            return result
        
        print(f"Job ID: {job_id}")
        print("Polling for completion...")
        
        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            status_response = requests.get(
                f"{url}/{job_id}",
                headers=headers
            )
            status_response.raise_for_status()
            status_result = status_response.json()
            
            status = status_result.get("status")
            print(f"Status: {status}")
            
            if status == "succeeded":
                print("Video generation complete!")
                
                # Download video if save_path provided
                video_url = status_result.get("output", {}).get("url")
                if video_url and save_path:
                    self._download_video(video_url, save_path)
                
                return status_result
            
            elif status == "failed":
                error_msg = status_result.get("error", "Unknown error")
                raise Exception(f"Video generation failed: {error_msg}")
            
            # Still processing
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Video generation timed out after {max_wait_time} seconds")
    
    def image_to_video(
        self,
        image_path: str,
        prompt: str,
        model: str = "veo-3",
        duration: int = 5,
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        fps: int = 24,
        motion_strength: float = 0.5,
        save_path: Optional[str] = None,
        poll_interval: int = 10,
        max_wait_time: int = 600,
    ) -> Dict:
        """
        Generate a video from an image and prompt.
        
        Args:
            image_path: Path to the input image
            prompt: Text description of desired video motion/content
            model: Model to use
            duration: Video duration in seconds
            resolution: Video resolution
            aspect_ratio: Aspect ratio
            fps: Frames per second
            motion_strength: How much motion to apply (0.0 to 1.0)
            save_path: Optional path to save the video
            poll_interval: Seconds between status checks
            max_wait_time: Maximum wait time in seconds
            
        Returns:
            Dictionary with video URL and metadata
        """
        url = f"{self.base_url}/videos/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Prepare multipart form data
        files = {
            'image': open(image_path, 'rb'),
        }
        
        data = {
            'prompt': prompt,
            'model': model,
            'duration': duration,
            'resolution': resolution,
            'aspect_ratio': aspect_ratio,
            'fps': fps,
            'motion_strength': motion_strength,
        }
        
        print(f"Starting image-to-video generation...")
        print(f"Image: {image_path}")
        print(f"Prompt: {prompt[:100]}...")
        
        # Submit generation request
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        
        result = response.json()
        job_id = result.get("id")
        
        if not job_id:
            print("Warning: No job ID returned, returning result as-is")
            return result
        
        print(f"Job ID: {job_id}")
        print("Polling for completion...")
        
        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            status_response = requests.get(
                f"{url}/{job_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            status_response.raise_for_status()
            status_result = status_response.json()
            
            status = status_result.get("status")
            print(f"Status: {status}")
            
            if status == "succeeded":
                print("Video generation complete!")
                
                # Download video if save_path provided
                video_url = status_result.get("output", {}).get("url")
                if video_url and save_path:
                    self._download_video(video_url, save_path)
                
                return status_result
            
            elif status == "failed":
                error_msg = status_result.get("error", "Unknown error")
                raise Exception(f"Video generation failed: {error_msg}")
            
            # Still processing
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Video generation timed out after {max_wait_time} seconds")
    
    def get_job_status(self, job_id: str) -> Dict:
        """
        Get the status of a video generation job.
        
        Args:
            job_id: The job ID to check
            
        Returns:
            Dictionary with job status and details
        """
        url = f"{self.base_url}/videos/generations/{job_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def _download_video(self, video_url: str, save_path: str):
        """
        Download video from URL to local path.
        
        Args:
            video_url: URL of the video
            save_path: Local path to save to
        """
        print(f"Downloading video from: {video_url}")
        
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Video saved to: {save_path}")


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_text_to_video(client: ThucChienClient):
    """Example: Generate a video from text"""
    generator = VideoGenerator(client)
    
    prompt = """A cinematic shot of a lone astronaut walking on Mars, 
    red dust swirling around them, two moons visible in the pink sky, 
    dramatic lighting from the setting sun, wide angle lens, 
    science fiction movie aesthetic."""
    
    result = generator.text_to_video(
        prompt=prompt,
        model="veo-3",
        duration=5,
        resolution="1080p",
        aspect_ratio="16:9",
        save_path="outputs/mars_astronaut.mp4",
    )
    
    print("Video generated successfully!")
    return result


def example_text_to_video_with_dialogue(client: ThucChienClient):
    """Example: Generate video with dialogue and sound"""
    generator = VideoGenerator(client)
    
    prompt = """Two detectives in a dimly lit office reviewing case files. 
    "We're missing something," the first detective says, pointing at a photo. 
    "Look at this shadow here," the second responds, leaning closer. 
    Tense atmosphere, film noir style, dramatic lighting from a desk lamp, 
    papers scattered on the desk, coffee cups, city lights visible through window."""
    
    result = generator.text_to_video(
        prompt=prompt,
        model="veo-3",
        duration=8,
        resolution="1080p",
        save_path="outputs/detective_scene.mp4",
    )
    
    print("Video with dialogue generated!")
    return result


def example_image_to_video(client: ThucChienClient):
    """Example: Animate a still image"""
    generator = VideoGenerator(client)
    
    prompt = "The ocean waves gently roll onto the beach, palm trees sway in the breeze"
    
    result = generator.image_to_video(
        image_path="outputs/beach_sunset.jpg",
        prompt=prompt,
        model="veo-3",
        duration=5,
        motion_strength=0.7,
        save_path="outputs/animated_beach.mp4",
    )
    
    print("Image animated successfully!")
    return result


def example_cinematic_shot(client: ThucChienClient):
    """Example: Create a cinematic video with camera movement"""
    generator = VideoGenerator(client)
    
    prompt = """A smooth tracking shot following a sports car driving through 
    a neon-lit cyberpunk city at night. The camera dollies alongside the car 
    as it weaves through traffic, holographic billboards reflecting off the 
    wet pavement, rain falling, bokeh effect from city lights, 
    vibrant purple and blue color grading, cinematic 2.35:1 aspect ratio feel."""
    
    result = generator.text_to_video(
        prompt=prompt,
        model="veo-3",
        duration=10,
        resolution="1080p",
        aspect_ratio="16:9",
        fps=30,
        save_path="outputs/cyberpunk_car_chase.mp4",
    )
    
    print("Cinematic shot generated!")
    return result


def example_animated_character(client: ThucChienClient):
    """Example: Generate 3D animated character video"""
    generator = VideoGenerator(client)
    
    prompt = """A cute 3D animated character, a small blue dragon with big eyes, 
    happily bouncing through a magical forest. The dragon discovers a glowing 
    crystal and tilts its head in curiosity. Pixar-style animation, 
    bright cheerful colors, soft lighting, whimsical atmosphere."""
    
    result = generator.text_to_video(
        prompt=prompt,
        model="veo-3",
        duration=6,
        resolution="1080p",
        save_path="outputs/cute_dragon.mp4",
    )
    
    print("Animated character video generated!")
    return result


def example_product_showcase(client: ThucChienClient):
    """Example: Product showcase video"""
    generator = VideoGenerator(client)
    
    prompt = """A sleek modern smartphone rotating on a pedestal against 
    a minimalist white background. Studio lighting with soft shadows, 
    the phone screen displays a vibrant colorful interface, 
    camera slowly orbits around the product, professional product photography style, 
    clean and premium aesthetic."""
    
    result = generator.text_to_video(
        prompt=prompt,
        model="veo-3",
        duration=5,
        resolution="1080p",
        save_path="outputs/phone_showcase.mp4",
    )
    
    print("Product showcase video generated!")
    return result


def example_nature_scene(client: ThucChienClient):
    """Example: Nature documentary style video"""
    generator = VideoGenerator(client)
    
    prompt = """A serene nature scene: a family of deer grazing in a misty meadow 
    at dawn, golden sunlight filtering through the trees, 
    gentle fog rolling across the grass, birds flying in the background, 
    documentary style cinematography, 4K quality, peaceful and tranquil atmosphere."""
    
    result = generator.text_to_video(
        prompt=prompt,
        model="veo-3",
        duration=8,
        resolution="1080p",
        save_path="outputs/nature_deer.mp4",
    )
    
    print("Nature scene generated!")
    return result


# =============================================================================
# BEST PRACTICES AND TIPS
# =============================================================================

"""
VIDEO GENERATION BEST PRACTICES:

1. Prompt Structure:
   Essential elements for good video prompts:
   - Subject: What or who is in the scene
   - Action: What is happening
   - Camera movement: tracking shot, dolly in, pan, static, etc.
   - Camera angle: aerial, close-up, wide shot, POV
   - Lighting: golden hour, studio lighting, dramatic, natural
   - Style: cinematic, documentary, animation style, film noir
   - Mood/Atmosphere: tense, peaceful, energetic, mysterious

2. Camera Techniques:
   Movement:
   - "tracking shot" - follows subject
   - "dolly in/out" - moves toward/away
   - "pan left/right" - rotates horizontally
   - "tilt up/down" - rotates vertically
   - "zoom in/out" - changes focal length
   - "crane shot" - moves up/down
   - "orbit" - circles around subject
   
   Angles:
   - "aerial view" - from above
   - "eye-level" - straight on
   - "low angle" - from below looking up
   - "high angle" - from above looking down
   - "POV shot" - first person perspective
   - "over-the-shoulder" - behind character

3. Adding Audio/Dialogue:
   - Use quotation marks for spoken dialogue
   - Describe ambient sounds: "wind howling", "traffic noise"
   - Specify sound effects: "footsteps echoing", "glass breaking"
   - Note: Audio generation availability depends on model

4. Style Keywords:
   - Cinematic: "film noir", "blockbuster", "indie film"
   - Animation: "3D cartoon", "Pixar style", "anime"
   - Documentary: "nature documentary", "historical footage"
   - Commercial: "product video", "advertisement"
   - Artistic: "surreal", "abstract", "impressionist"

5. Duration Guidelines:
   - 3-5 seconds: Simple actions, product shots
   - 5-8 seconds: Single scene with movement
   - 8-10 seconds: Complex scene or multiple actions
   - Longer videos may require scene breaks

6. Resolution Recommendations:
   - 720p: Faster generation, good for previews
   - 1080p: Standard HD, good quality
   - 4K: Best quality, longer generation time

7. Aspect Ratios:
   - 16:9: Standard video, YouTube, landscape
   - 9:16: Vertical video, TikTok, Instagram Stories
   - 1:1: Square video, Instagram Feed
   - 21:9: Ultra-wide, cinematic

8. Image-to-Video Tips:
   - Use clear, high-quality starting images
   - Prompt should describe desired motion/animation
   - Motion strength: 0.3-0.5 for subtle, 0.6-0.8 for dynamic
   - Ensure image aspect ratio matches video aspect ratio

9. Common Issues:
   - Too many actions in one prompt = confused output
   - Vague descriptions = unpredictable results
   - Missing camera info = static or random camera
   - Complex scenes may take longer to generate

10. Optimization Tips:
    - Be specific about camera work
    - Include lighting information
    - Specify style/aesthetic
    - Test with shorter durations first
    - Iterate on prompts for best results
    - Save successful prompt templates

EXAMPLE PROMPT TEMPLATE:

[Camera Movement] [Shot Type] of [Subject] [Action] in [Setting],
[Lighting], [Style], [Mood], [Audio Elements].

Example:
"A slow dolly-in shot of a chef preparing pasta in a rustic Italian kitchen,
warm golden lighting from the window, documentary style, peaceful atmosphere,
gentle classical music and cooking sounds."
"""


if __name__ == "__main__":
    try:
        client = ThucChienClient()
        
        print("=" * 80)
        print("Example: Text-to-Video Generation")
        print("=" * 80)
        example_text_to_video(client)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.")
    except Exception as e:
        print(f"Error: {e}")

