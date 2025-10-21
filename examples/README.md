# ThucChien.ai SDK Examples

This directory contains example scripts demonstrating various features of the ThucChien.ai SDK.

## Prerequisites

1. Install the SDK and dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Set up your API key:
   ```bash
   export THUCCHIEN_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file in the project root with:
   ```
   THUCCHIEN_API_KEY=your-api-key-here
   ```

## Examples

### 1. Text Generation (`chat_terminal.py`)
Interactive terminal chat using text generation.

**Run:**
```bash
python examples/chat_terminal.py
```

**Features:**
- Multi-turn conversations
- Streaming responses
- System message configuration

---

### 2. Image Generation (`image_generation_example.py`)
Demonstrates image generation and editing capabilities.

**Run:**
```bash
python examples/image_generation_example.py
```

**Features:**
- Standard text-to-image generation
- Chat-based image generation
- Image editing with prompts
- Multiple aspect ratios and sizes

**Output:** Images saved in `outputs/` folder

---

### 3. Text-to-Speech (`text_to_speech_example.py`)
Convert text to natural-sounding speech.

**Run:**
```bash
python examples/text_to_speech_example.py
```

**Features:**
- Male and female voices
- Different text lengths
- High-quality audio generation

**Output:** Audio files (.mp3) saved in `outputs/` folder

---

### 4. Video Generation (`video_generation_example.py`)
Generate videos from text and images.

**Run:**
```bash
python examples/video_generation_example.py
```

**Features:**
- Text-to-video generation
- Image-to-video animation
- Image-to-image transition (first frame → last frame)
- Multiple aspect ratios (16:9, 9:16)
- 8-second video clips with audio support

**Output:** Video files (.mp4) saved in `outputs/` folder

**Note:** Video generation takes several minutes per video.

---

### 5. Complete Workflow (`complete_workflow.py`)
Vietnamese Independence Day TV News Report - A complete 30-second production workflow.

**Run:**
```bash
python examples/complete_workflow.py
```

**Workflow:**
1. **Text Generation** - Creates Vietnamese news script about Independence Day (September 2nd)
2. **Image Generation** - Creates Vietnamese female reporter in áo dài
3. **Text-to-Speech** - Generates Vietnamese narration with female voice
4. **Video Generation** - Creates 4 video clips (8 seconds each = ~32 seconds total)
5. **Assembly Script** - Provides automated script to combine clips with audio

**Output:** All files saved in `outputs/vietnam_reporter/` folder:
- `news_script.txt` - Vietnamese news script
- `reporter_1.png` - Image of Vietnamese reporter
- `narration.mp3` - Vietnamese voice-over
- `clip_1.mp4` to `clip_4.mp4` - Video segments
- `assemble_video.sh` - Script to combine everything
- `ASSEMBLY_INSTRUCTIONS.md` - Detailed assembly guide

**Final Assembly:**
```bash
cd outputs/vietnam_reporter
./assemble_video.sh
```

**Requirements:** FFmpeg for video assembly (install: `brew install ffmpeg`)

**Note:** This workflow takes 20-30 minutes to generate all clips, but produces a professional news segment with synchronized Vietnamese audio and video.

---

## Tips

- **Outputs Folder**: All examples automatically create an `outputs/` directory for generated files
- **API Quotas**: Be mindful of API usage, especially for video generation
- **Experimentation**: Modify prompts and parameters in the examples to explore different results
- **Dependencies**: Some examples depend on outputs from others (e.g., video generation can use images from image generation)

## Running All Examples

To run all examples in sequence:

```bash
python examples/image_generation_example.py
python examples/text_to_speech_example.py
python examples/video_generation_example.py
python examples/complete_workflow.py
```

## Troubleshooting

- **API Key Error**: Make sure `THUCCHIEN_API_KEY` is set correctly
- **Import Errors**: Install the SDK from the project root: `pip install -e .`
- **Video Generation Timeout**: Video generation can take 5-10 minutes; be patient
- **File Not Found**: Some examples require previous examples to run first

## Support

For issues or questions, please refer to the main README.md or visit [thucchien.ai](https://thucchien.ai).

