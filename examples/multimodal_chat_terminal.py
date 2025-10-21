#!/usr/bin/env python3
"""
Interactive Multi-turn Multimodal Chat Terminal
Supports text and image inputs, generates text and image outputs with various aspect ratios.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thucchien_ai_sdk import ThucChienClient
from thucchien_ai_sdk.image_generation import ImageGenerator


class MultimodalChatTerminal:
    """Interactive terminal for multimodal chat with image generation."""
    
    ASPECT_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9"]
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize the chat terminal.
        
        Args:
            client: ThucChienClient instance
        """
        self.client = client
        self.generator = ImageGenerator(client)
        self.conversation = None
        self.output_dir = Path("outputs/chat_session")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.image_counter = 0
    
    def print_header(self):
        """Print welcome header."""
        print("=" * 80)
        print("🎨 MULTIMODAL CHAT TERMINAL 🎨")
        print("=" * 80)
        print("\nFeatures:")
        print("  • Multi-turn conversations with context")
        print("  • Text and image inputs")
        print("  • Image generation with multiple aspect ratios")
        print("  • Text and image outputs")
        print("\nSupported aspect ratios: 1:1, 3:4, 4:3, 9:16, 16:9")
        print("\nCommands:")
        print("  /image <path>       - Add an image to your message")
        print("  /ratio <ratio>      - Set aspect ratio for image generation")
        print("  /clear              - Clear conversation history")
        print("  /history            - Show conversation history")
        print("  /help               - Show this help message")
        print("  /quit or /exit      - Exit the chat")
        print("\nExamples:")
        print("  Generate an image:")
        print("    > /ratio 16:9")
        print("    > A beautiful sunset over mountains")
        print("\n  Analyze an image:")
        print("    > /image path/to/image.png")
        print("    > What's in this image?")
        print("\n  Edit an image:")
        print("    > /image path/to/image.png")
        print("    > /ratio 1:1")
        print("    > Make this more vibrant and add a rainbow")
        print("=" * 80)
        print()
    
    def print_help(self):
        """Print help message."""
        print("\n📖 HELP")
        print("-" * 80)
        print("Commands:")
        print("  /image <path>       - Add image(s) to message (can be used multiple times)")
        print("  /ratio <ratio>      - Set aspect ratio (1:1, 3:4, 4:3, 9:16, 16:9)")
        print("  /clear              - Clear conversation history")
        print("  /history            - Show message count")
        print("  /help               - Show this help")
        print("  /quit, /exit        - Exit chat")
        print("\nUsage Tips:")
        print("  • Start conversation with a greeting or directly ask for image generation")
        print("  • Use /ratio before requesting image generation to set output format")
        print("  • Include images with /image to ask questions or request edits")
        print("  • Be specific in your prompts for better results")
        print("-" * 80)
        print()
    
    def start_conversation(self):
        """Start a new conversation."""
        system_message = """You are a helpful AI assistant with image generation capabilities.
You can understand images, generate new images based on descriptions, and help with 
image editing tasks. When users ask for images, create them with detailed, creative prompts."""
        
        self.conversation = self.generator.create_conversation(
            system_message=system_message,
            model="gemini-2.5-flash-image-preview"
        )
        print("✅ New conversation started!\n")
    
    def parse_input(self, user_input: str):
        """
        Parse user input to extract text, commands, and parameters.
        
        Returns:
            tuple: (text, image_paths, aspect_ratio, command)
        """
        lines = user_input.strip().split('\n')
        text_parts = []
        image_paths = []
        aspect_ratio = None
        command = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('/'):
                parts = line.split(maxsplit=1)
                cmd = parts[0].lower()
                
                if cmd in ['/quit', '/exit']:
                    command = 'quit'
                elif cmd == '/help':
                    command = 'help'
                elif cmd == '/clear':
                    command = 'clear'
                elif cmd == '/history':
                    command = 'history'
                elif cmd == '/image' and len(parts) > 1:
                    img_path = parts[1].strip()
                    if os.path.exists(img_path):
                        image_paths.append(img_path)
                    else:
                        print(f"⚠️  Warning: Image not found: {img_path}")
                elif cmd == '/ratio' and len(parts) > 1:
                    ratio = parts[1].strip()
                    if ratio in self.ASPECT_RATIOS:
                        aspect_ratio = ratio
                    else:
                        print(f"⚠️  Warning: Invalid aspect ratio. Use one of: {', '.join(self.ASPECT_RATIOS)}")
                else:
                    print(f"⚠️  Unknown command: {cmd}")
            else:
                text_parts.append(line)
        
        text = '\n'.join(text_parts) if text_parts else None
        return text, image_paths, aspect_ratio, command
    
    def format_response(self, result: dict):
        """
        Format and display the response.
        
        Args:
            result: API response dictionary
        """
        try:
            message = result['choices'][0]['message']
            
            # Display text content
            if 'content' in message and message['content']:
                print(f"\n🤖 Assistant: {message['content']}")
            
            # Display generated images info
            if 'images' in message and message['images']:
                print(f"\n🖼️  Generated {len(message['images'])} image(s)")
                for i, img in enumerate(message['images'], 1):
                    if 'saved_path' in result:
                        print(f"   {i}. Saved to: {result['saved_path']}")
            
            print()
            
        except (KeyError, IndexError) as e:
            print(f"⚠️  Error parsing response: {e}")
            print(f"Raw response: {result}")
    
    def run(self):
        """Run the interactive chat loop."""
        self.print_header()
        self.start_conversation()
        
        current_aspect_ratio = None
        
        while True:
            try:
                # Get user input
                print("💬 You: ", end="", flush=True)
                user_input = input()
                
                if not user_input.strip():
                    continue
                
                # Parse input
                text, image_paths, aspect_ratio, command = self.parse_input(user_input)
                
                # Update aspect ratio if specified
                if aspect_ratio:
                    current_aspect_ratio = aspect_ratio
                    print(f"📐 Aspect ratio set to: {current_aspect_ratio}")
                
                # Handle commands
                if command == 'quit':
                    print("\n👋 Goodbye!")
                    break
                elif command == 'help':
                    self.print_help()
                    continue
                elif command == 'clear':
                    self.start_conversation()
                    current_aspect_ratio = None
                    print("🗑️  Conversation history cleared!")
                    continue
                elif command == 'history':
                    history = self.conversation.get_history()
                    print(f"📝 Conversation has {len(history)} message(s)")
                    continue
                
                # Must have text or images to send
                if not text and not image_paths:
                    continue
                
                # Show what we're sending
                if image_paths:
                    print(f"📎 Including {len(image_paths)} image(s)")
                if current_aspect_ratio:
                    print(f"📐 Using aspect ratio: {current_aspect_ratio}")
                
                # Generate save path for potential image output
                self.image_counter += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = self.output_dir / f"generated_{timestamp}_{self.image_counter}.png"
                
                # Send message
                print("\n⏳ Processing...", end="", flush=True)
                result = self.conversation.send(
                    text=text,
                    image_paths=image_paths if image_paths else None,
                    aspect_ratio=current_aspect_ratio,
                    save_path=str(save_path),
                )
                print("\r" + " " * 20 + "\r", end="")  # Clear "Processing..."
                
                # Display response
                self.format_response(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                print()


def main():
    """Main entry point."""
    try:
        # Initialize client
        client = ThucChienClient()
        
        # Start chat terminal
        terminal = MultimodalChatTerminal(client)
        terminal.run()
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set THUCCHIEN_API_KEY environment variable.")
        print("\nExample:")
        print("  export THUCCHIEN_API_KEY='your-api-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

