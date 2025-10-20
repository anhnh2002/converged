# Quick Start Guide

Get started with ThucChien AI SDK in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/thucchien-ai-sdk.git
cd thucchien-ai-sdk

# Install dependencies
pip install -r requirements.txt
```

## Setup API Key

Get your API key from [ThucChien.ai](https://thucchien.ai) and set it:

```bash
export THUCCHIEN_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```bash
cp env.example .env
# Edit .env and add your API key
```

## First Example - Text Generation

```python
from thucchien_ai_sdk import ThucChienClient, TextGenerator

# Initialize
client = ThucChienClient()
generator = TextGenerator(client)

# Generate text
response = generator.generate("Write a haiku about AI")
print(response)
```

## Multi-turn Conversation

```python
# Create a conversation
conversation = generator.create_conversation(
    system_message="You are a helpful assistant"
)

# Chat
response1 = conversation.send("What is Python?")
response2 = conversation.send("Show me an example")
response3 = conversation.send("Explain more about that")
```

## Generate an Image

```python
from thucchien_ai_sdk import ImageGenerator

img_gen = ImageGenerator(client)

result = img_gen.text_to_image(
    prompt="A beautiful sunset over mountains",
    save_path="outputs/sunset.png"
)
```

## Create a Video

```python
from thucchien_ai_sdk import VideoGenerator

video_gen = VideoGenerator(client)

result = video_gen.text_to_video(
    prompt="Ocean waves rolling onto a beach",
    duration=5,
    save_path="outputs/ocean.mp4"
)
```

## Text-to-Speech

```python
from thucchien_ai_sdk import TextToSpeech

tts = TextToSpeech(client)

result = tts.generate(
    text="Hello, world!",
    voice="alloy",
    save_path="outputs/hello.mp3"
)
```

## Run Examples

```bash
# Text generation examples
python examples/text_generation_demo.py

# Image generation examples
python examples/image_generation_demo.py

# Video generation examples
python examples/video_generation_demo.py

# Text-to-speech examples
python examples/text_to_speech_demo.py

# Complete workflow
python examples/complete_workflow.py
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [examples/](examples/) directory for more use cases
- Check out the API documentation at [docs.thucchien.ai](https://docs.thucchien.ai)

## Common Issues

**Problem**: `ValueError: API key is required`
**Solution**: Set the `THUCCHIEN_API_KEY` environment variable

**Problem**: `ModuleNotFoundError: No module named 'openai'`
**Solution**: Run `pip install -r requirements.txt`

**Problem**: Video generation times out
**Solution**: Increase `max_wait_time` parameter or check API status

## Support

- Documentation: https://docs.thucchien.ai
- Issues: https://github.com/yourusername/thucchien-ai-sdk/issues

