#!/usr/bin/env python3
"""
Interactive Text Chat Terminal
Simple multi-turn conversation interface with AI.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thucchien_ai_sdk import ThucChienClient
from thucchien_ai_sdk.text_generation import TextGenerator


class ChatTerminal:
    """Interactive terminal for text-based multi-turn conversations."""
    
    MODELS = {
        '1': ('gemini-2.5-flash', 'Gemini 2.5 Flash (Fast)'),
        '2': ('gemini-2.5-pro', 'Gemini 2.5 Pro (Advanced)'),
    }
    
    def __init__(self, client: ThucChienClient):
        """
        Initialize the chat terminal.
        
        Args:
            client: ThucChienClient instance
        """
        self.client = client
        self.generator = TextGenerator(client)
        self.conversation = None
        self.current_model = "gemini-2.5-flash"
        self.temperature = 0.7
    
    def print_header(self):
        """Print welcome header."""
        print("\n" + "=" * 80)
        print("💬 AI CHAT TERMINAL 💬")
        print("=" * 80)
        print("\nWelcome to the interactive AI chat terminal!")
        print("Have multi-turn conversations with AI models.\n")
        print("Commands:")
        print("  /help               - Show this help message")
        print("  /clear              - Clear conversation history")
        print("  /history            - Show conversation history")
        print("  /model              - Change AI model")
        print("  /temp <0.0-2.0>     - Set temperature (randomness)")
        print("  /system <message>   - Set system message and restart conversation")
        print("  /quit or /exit      - Exit the chat")
        print("\nTip: Just type your message and press Enter to chat!")
        print("=" * 80)
        print()
    
    def print_help(self):
        """Print help message."""
        print("\n📖 HELP")
        print("-" * 80)
        print("Commands:")
        print("  /help               - Show this help message")
        print("  /clear              - Clear conversation history (keeps system message)")
        print("  /history            - Show all messages in the conversation")
        print("  /model              - Change AI model")
        print("  /temp <value>       - Set temperature (0.0-2.0, default: 0.7)")
        print("  /system <message>   - Set system message and restart conversation")
        print("  /quit, /exit        - Exit the chat")
        print("\nAbout Temperature:")
        print("  • Lower (0.0-0.5): More focused and deterministic")
        print("  • Medium (0.5-1.0): Balanced creativity")
        print("  • Higher (1.0-2.0): More creative and random")
        print("\nAbout System Messages:")
        print("  System messages set the context and behavior of the AI.")
        print("  Example: /system You are a helpful coding assistant")
        print("-" * 80)
        print()
    
    def select_model(self):
        """Allow user to select a model."""
        print("\n🤖 Select Model:")
        print("-" * 80)
        for key, (model_id, name) in self.MODELS.items():
            current = " (current)" if model_id == self.current_model else ""
            print(f"  {key}. {name}{current}")
        print("-" * 80)
        
        choice = input("Enter choice (or press Enter to cancel): ").strip()
        
        if choice in self.MODELS:
            self.current_model = self.MODELS[choice][0]
            print(f"✅ Model changed to: {self.MODELS[choice][1]}")
            
            # Restart conversation with new model
            self.start_conversation()
        elif choice:
            print("❌ Invalid choice")
    
    def start_conversation(self, system_message: str = None):
        """
        Start a new conversation.
        
        Args:
            system_message: Optional system message to set context
        """
        if system_message is None:
            system_message = "You are a helpful, friendly AI assistant."
        
        self.conversation = self.generator.create_conversation(
            system_message=system_message,
            model=self.current_model
        )
        print(f"✅ Conversation started with {self.current_model}")
        if system_message != "You are a helpful, friendly AI assistant.":
            print(f"📝 System: {system_message}")
        print()
    
    def show_history(self):
        """Display conversation history."""
        history = self.conversation.get_history()
        
        print("\n📜 CONVERSATION HISTORY")
        print("-" * 80)
        
        if not history:
            print("(No messages yet)")
        else:
            for i, msg in enumerate(history, 1):
                role = msg['role'].upper()
                content = msg['content']
                
                # Color code by role
                if role == 'SYSTEM':
                    print(f"\n[{i}] 📋 {role}:")
                    print(f"    {content}")
                elif role == 'USER':
                    print(f"\n[{i}] 👤 {role}:")
                    print(f"    {content}")
                elif role == 'ASSISTANT':
                    print(f"\n[{i}] 🤖 {role}:")
                    # Print with indentation for long responses
                    for line in content.split('\n'):
                        print(f"    {line}")
        
        print("\n" + "-" * 80)
        print(f"Total messages: {len(history)}\n")
    
    def handle_command(self, command: str) -> bool:
        """
        Handle special commands.
        
        Args:
            command: The command string (starting with /)
            
        Returns:
            True if should continue, False if should quit
        """
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None
        
        if cmd in ['/quit', '/exit']:
            print("\n👋 Goodbye! Thanks for chatting!")
            return False
        
        elif cmd == '/help':
            self.print_help()
        
        elif cmd == '/clear':
            self.conversation.clear_history(keep_system=True)
            print("🗑️  Conversation history cleared! (System message kept)\n")
        
        elif cmd == '/history':
            self.show_history()
        
        elif cmd == '/model':
            self.select_model()
        
        elif cmd == '/temp':
            if arg:
                try:
                    temp = float(arg)
                    if 0.0 <= temp <= 2.0:
                        self.temperature = temp
                        print(f"🌡️  Temperature set to: {temp}\n")
                    else:
                        print("❌ Temperature must be between 0.0 and 2.0\n")
                except ValueError:
                    print("❌ Invalid temperature value\n")
            else:
                print(f"Current temperature: {self.temperature}\n")
        
        elif cmd == '/system':
            if arg:
                self.start_conversation(system_message=arg)
            else:
                print("❌ Please provide a system message\n")
        
        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type /help for available commands\n")
        
        return True
    
    def run(self):
        """Run the interactive chat loop."""
        self.print_header()
        self.start_conversation()
        
        while True:
            try:
                # Get user input
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    should_continue = self.handle_command(user_input)
                    if not should_continue:
                        break
                    continue
                
                # Send message and get response
                print("\n⏳ Thinking...", end="", flush=True)
                
                response = self.conversation.send(
                    message=user_input,
                    temperature=self.temperature
                )
                
                # Clear the "Thinking..." message
                print("\r" + " " * 20 + "\r", end="")
                
                # Display response
                print("🤖 Assistant:", end="")
                
                # Print response with nice formatting
                lines = response.split('\n')
                for i, line in enumerate(lines):
                    if i == 0:
                        print(f" {line}")
                    else:
                        print(f"              {line}")
                
                print()  # Extra newline for readability
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting!")
                break
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.\n")


def main():
    """Main entry point."""
    try:
        # Initialize client
        client = ThucChienClient()
        
        # Start chat terminal
        terminal = ChatTerminal(client)
        terminal.run()
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set THUCCHIEN_API_KEY environment variable.")
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

