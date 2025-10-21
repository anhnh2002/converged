# ThucChien AI SDK

A comprehensive Python SDK for the [ThucChien.ai](https://thucchien.ai) API, providing easy access to state-of-the-art AI capabilities including text generation, image generation and editing, video generation, and text-to-speech.

## Features

- 🤖 **Text Generation**: Single-turn and multi-turn conversations with GPT models
- 🎨 **Image Generation**: Create images from text with DALL-E models
- ✏️ **Image Editing**: Edit existing images
- 🎬 **Video Generation**: Generate videos from text or animate images
- 🔊 **Text-to-Speech**: Convert text to natural-sounding speech with multiple voices
- 💬 **Multi-turn Conversations**: Maintain conversation context across multiple interactions
- 📝 **Session Management**: Handle complex multi-step creative workflows

## Installation

### From Source

```bash
git clone https://github.com/yourusername/thucchien-ai-sdk.git
cd thucchien-ai-sdk
pip install -r requirements.txt
```

### Install Dependencies

```bash
pip install openai requests Pillow python-dotenv
```

## Quick Start

### Setup

First, obtain your API key from [ThucChien.ai](https://thucchien.ai) and set it as an environment variable:

```bash
export THUCCHIEN_API_KEY="your-api-key-here"
```

Or use a `.env` file:

```env
THUCCHIEN_API_KEY=your-api-key-here
```

### Basic Usage

```python
from thucchien_ai_sdk import ThucChienClient, TextGenerator, ImageGenerator

# Initialize client
client = ThucChienClient()

# Text Generation
generator = TextGenerator(client)
response = generator.generate("Write a poem about AI")
print(response)

# Image Generation
img_generator = ImageGenerator(client)
result = img_generator.text_to_image(
    prompt="A serene mountain landscape at sunset",
    save_path="outputs/mountain.png"
)
```

## Documentation

### Text Generation

#### Simple Generation

```python
from thucchien_ai_sdk import ThucChienClient, TextGenerator

client = ThucChienClient()
generator = TextGenerator(client)

# Generate text
response = generator.generate(
    prompt="Explain quantum computing in simple terms",
    temperature=0.7,
    max_tokens=500
)
print(response)
```

#### Multi-turn Conversation

```python
# Create a conversation session
conversation = generator.create_conversation(
    system_message="You are a helpful coding assistant",
    model="gpt-4"
)

# Have a conversation
response1 = conversation.send("What is a Python decorator?")
response2 = conversation.send("Can you show me an example?")
response3 = conversation.send("How is this different from a function wrapper?")

# Get conversation history
history = conversation.get_history()
```

#### Streaming Responses

```python
messages = [{"role": "user", "content": "Write a short story"}]
stream = generator.chat(messages=messages, stream=True)

for chunk in stream:
    if chunk.choices[0].delta.get("content"):
        print(chunk.choices[0].delta["content"], end="", flush=True)
```

### Image Generation

#### Chat-based Image Generation (Gemini)

Generate images through the chat completions endpoint using Gemini models with support for aspect ratios and input images:

```python
from thucchien_ai_sdk import ThucChienClient, ImageGenerator

client = ThucChienClient()
img_generator = ImageGenerator(client)

# Generate image via chat endpoint with aspect ratio
result = img_generator.chat_generate_image(
    prompt="A futuristic cityscape at sunset with flying cars and neon lights",
    model="gemini-2.5-flash-image-preview",
    aspect_ratio="16:9",  # Supported: "1:1", "3:4", "4:3", "9:16", "16:9"
    save_path="outputs/city.png"
)

# Generate image with input image
result = img_generator.chat_generate_image(
    prompt="Make this image more vibrant and add a sunset",
    input_images=["path/to/image.png"],
    aspect_ratio="1:1",
    save_path="outputs/edited.png"
)
```

#### Multimodal Conversation

Create multi-turn conversations with text and image inputs/outputs:

```python
# Create a multimodal conversation
conversation = img_generator.create_conversation(
    system_message="You are a creative AI assistant."
)

# Turn 1: Generate an image
result1 = conversation.send(
    text="Create a cute cat",
    aspect_ratio="1:1",
    save_path="outputs/cat_v1.png"
)

# Turn 2: Modify based on context
result2 = conversation.send(
    text="Now add a wizard hat",
    aspect_ratio="1:1",
    save_path="outputs/cat_v2.png"
)

# Turn 3: Include an input image
result3 = conversation.send(
    text="Make this cat sit in a magical forest",
    image_paths=["outputs/existing_image.png"],
    aspect_ratio="16:9",
    save_path="outputs/cat_v3.png"
)
```

#### Text-to-Image (DALL-E)

```python
# Generate image with DALL-E
result = img_generator.text_to_image(
    prompt="A futuristic city with flying cars at night",
    model="imagen-4",
    save_path="outputs/futuristic_city.png"
)
```

#### Image Editing

```python
# Edit an existing image
result = img_generator.edit_image(
    image_path="outputs/landscape.png",
    prompt="Add a rainbow in the sky",
    save_path="outputs/landscape_with_rainbow.png"
)
```

#### Multi-turn Image Editing

```python
# Create an editing session
session = img_generator.create_editing_session()

# Generate and iteratively edit
session.generate(prompt="A modern living room")
session.generate(prompt="Add a grey sofa")
session.generate(prompt="Add plants by the window")

# Get editing history
history = session.get_history()
```

### Video Generation

#### Text-to-Video

```python
from thucchien_ai_sdk import ThucChienClient, VideoGenerator

client = ThucChienClient()
video_gen = VideoGenerator(client)

# Generate video
result = video_gen.text_to_video(
    prompt="A astronaut walking on Mars at sunset",
    model="veo-3",
    duration=5,
    resolution="1080p",
    aspect_ratio="16:9",
    save_path="outputs/mars_walk.mp4"
)
```

#### Image-to-Video

```python
# Animate a still image
result = video_gen.image_to_video(
    image_path="outputs/beach.jpg",
    prompt="Ocean waves rolling onto the beach, palm trees swaying",
    duration=5,
    motion_strength=0.7,
    save_path="outputs/beach_animated.mp4"
)
```

### Text-to-Speech

#### Simple TTS

```python
from thucchien_ai_sdk import ThucChienClient, TextToSpeech

client = ThucChienClient()
tts = TextToSpeech(client)

# Generate speech
result = tts.generate(
    text="Hello! Welcome to ThucChien AI.",
    voice="alloy",
    save_path="outputs/welcome.mp3"
)
```

#### Different Voices

```python
# Available voices: alloy, echo, fable, onyx, nova, shimmer
voices = ["alloy", "echo", "nova", "shimmer"]

for voice in voices:
    tts.generate(
        text="This is a voice sample.",
        voice=voice,
        save_path=f"outputs/sample_{voice}.mp3"
    )
```

#### Multiple Texts

```python
texts = [
    "Welcome to chapter one.",
    "Welcome to chapter two.",
    "Welcome to chapter three.",
]

results = tts.generate_multiple(
    texts=texts,
    voice="fable",
    model="tts-1-hd",
    output_dir="outputs"
)
```

## API Reference

### ThucChienClient

```python
client = ThucChienClient(api_key="your-key", base_url="https://api.thucchien.ai/v1")
```

### TextGenerator

- `generate(prompt, model, temperature, max_tokens, ...)` - Generate text
- `chat(messages, model, temperature, stream, ...)` - Multi-turn chat
- `create_conversation(system_message, model)` - Create conversation session

### ImageGenerator

- `chat_generate_image(prompt, model, save_path, messages, aspect_ratio, input_images)` - Generate via chat endpoint with aspect ratios and input images (Gemini)
- `text_to_image(prompt, model, size, quality, ...)` - Generate images (DALL-E)
- `edit_image(image_path, prompt, mask_path, ...)` - Edit images
- `create_conversation(system_message, model)` - Create multimodal conversation session
- `create_editing_session(initial_image_path, model)` - Multi-turn editing

### MultimodalConversation

- `send(text, image_paths, aspect_ratio, save_path)` - Send message with optional images and aspect ratio
- `get_history()` - Get conversation history
- `clear_history(keep_system)` - Clear conversation history

### VideoGenerator

- `text_to_video(prompt, model, duration, resolution, ...)` - Generate videos
- `image_to_video(image_path, prompt, motion_strength, ...)` - Animate images
- `get_job_status(job_id)` - Check generation status

### TextToSpeech

- `generate(text, model, voice, speed, ...)` - Generate speech
- `generate_from_file(file_path, model, voice, ...)` - TTS from file
- `generate_multiple(texts, voice, output_dir, ...)` - Batch generation
- `get_available_voices()` - List available voices

## Examples

See the `examples/` directory for complete working examples:

- `examples/text_generation_demo.py` - Text generation examples
- `examples/image_generation_demo.py` - Image generation examples
- `examples/multimodal_chat_demo.py` - Multimodal chat with images and aspect ratios
- `examples/multimodal_chat_terminal.py` - Interactive terminal chat interface
- `examples/video_generation_demo.py` - Video generation examples
- `examples/text_to_speech_demo.py` - TTS examples
- `examples/complete_workflow.py` - End-to-end creative workflow

### Interactive Terminal Chat

Run the interactive multimodal chat terminal:

```bash
python examples/multimodal_chat_terminal.py
```

Features:
- Multi-turn conversations with full context
- Text and image inputs
- Image generation with aspect ratios (1:1, 3:4, 4:3, 9:16, 16:9)
- Simple command-based interface

Example session:
```
💬 You: /ratio 16:9
💬 You: Create a beautiful mountain landscape

🤖 Assistant: [Generates image with 16:9 aspect ratio]

💬 You: /image outputs/existing.png
💬 You: Make this image look like it was painted by Van Gogh
```

## Advanced Usage

### Environment Configuration

```python
import os
from dotenv import load_dotenv
from thucchien_ai_sdk import ThucChienClient

load_dotenv()
client = ThucChienClient(api_key=os.getenv("THUCCHIEN_API_KEY"))
```

### Error Handling

```python
try:
    result = generator.generate(prompt="Hello")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

### Async Operations

Video generation is asynchronous. The SDK handles polling automatically:

```python
result = video_gen.text_to_video(
    prompt="A beautiful sunset",
    poll_interval=10,  # Check every 10 seconds
    max_wait_time=600  # Timeout after 10 minutes
)
```

## Best Practices

### Text Generation

- Use lower temperatures (0.3-0.5) for factual content
- Use higher temperatures (0.7-1.0) for creative content
- Provide clear system messages for consistent behavior
- Use streaming for long-form content

### Image Generation

- **Gemini Chat-based**: Use `chat_generate_image()` for conversational image generation
  - Returns base64-encoded images
  - Supports multi-turn refinement
  - Supports aspect ratios: "1:1", "3:4", "4:3", "9:16", "16:9"
  - Supports input images for editing and analysis
  - Model: `gemini-2.5-flash-image-preview`
- **Aspect Ratios**:
  - `1:1` - Square images, perfect for social media
  - `3:4` - Portrait orientation, good for prints
  - `4:3` - Standard photo ratio
  - `9:16` - Vertical/mobile, ideal for stories
  - `16:9` - Widescreen/landscape, great for banners
- Be specific and descriptive in prompts
- Include style keywords: "photorealistic", "oil painting", etc.
- Specify lighting and composition
- Use multimodal conversations for iterative refinement

### Video Generation

- Include camera movement in prompts: "tracking shot", "dolly in"
- Specify lighting and atmosphere
- Use dialogue in quotes for audio generation
- Test with shorter durations first

### Text-to-Speech

- Use proper punctuation for natural pauses
- Select appropriate voice for content type
- Use tts-1-hd for professional content
- Adjust speed for different use cases

## Troubleshooting

### Common Issues

**API Key Error**
```
Error: API key is required
```
Solution: Set `THUCCHIEN_API_KEY` environment variable

**Image Format Error**
```
Error: Image must be PNG format
```
Solution: Convert image to PNG before editing

**Video Timeout**
```
TimeoutError: Video generation timed out
```
Solution: Increase `max_wait_time` parameter

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

- Documentation: https://docs.thucchien.ai
- API Reference: https://api.thucchien.ai/docs
- Issues: https://github.com/yourusername/thucchien-ai-sdk/issues

## Acknowledgments

This SDK is built on top of the ThucChien.ai API, which is compatible with OpenAI's API standards.

---

Made with ❤️ for the AI community

