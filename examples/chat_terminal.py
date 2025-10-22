#!/usr/bin/env python3
"""
Interactive Text Chat Terminal
Simple multi-turn conversation interface with AI.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

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
        
        # Session management
        self.sessions_dir = Path('./.thucchien_chat_sessions')
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session_id = None
        self.session_metadata = {}
    
    def get_session_path(self, session_id: str) -> Path:
        """Get the file path for a session."""
        return self.sessions_dir / f"{session_id}.json"
    
    def list_sessions(self):
        """List all available sessions."""
        sessions = []
        for file_path in self.sessions_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    sessions.append({
                        'id': file_path.stem,
                        'metadata': data.get('metadata', {}),
                        'message_count': len(data.get('history', []))
                    })
            except Exception:
                continue
        
        # Sort by creation time (newest first)
        sessions.sort(key=lambda x: x['metadata'].get('created_at', ''), reverse=True)
        return sessions
    
    def save_session(self):
        """Save current session to disk."""
        if not self.current_session_id or not self.conversation:
            return
        
        session_data = {
            'metadata': self.session_metadata,
            'history': self.conversation.get_history(),
            'model': self.current_model,
            'temperature': self.temperature
        }
        
        session_path = self.get_session_path(self.current_session_id)
        with open(session_path, 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self, session_id: str) -> bool:
        """
        Load an existing session.
        
        Args:
            session_id: The session ID to load
            
        Returns:
            True if successful, False otherwise
        """
        session_path = self.get_session_path(session_id)
        
        if not session_path.exists():
            return False
        
        try:
            with open(session_path, 'r') as f:
                session_data = json.load(f)
            
            # Restore session state
            self.current_session_id = session_id
            self.session_metadata = session_data.get('metadata', {})
            self.current_model = session_data.get('model', 'gemini-2.5-flash')
            self.temperature = session_data.get('temperature', 0.7)
            
            # Get system message from history
            history = session_data.get('history', [])
            system_message = "You are a helpful, friendly AI assistant."
            
            if history and history[0]['role'] == 'system':
                system_message = history[0]['content']
            
            # Create new conversation
            self.conversation = self.generator.create_conversation(
                system_message=system_message,
                model=self.current_model
            )
            
            # Restore history (skip system message as it's already set)
            for msg in history[1:]:
                self.conversation.messages.append(msg)
            
            # Update metadata
            self.session_metadata['last_accessed'] = datetime.now().isoformat()
            self.save_session()
            
            return True
            
        except Exception as e:
            print(f"Error loading session: {e}")
            return False
    
    def create_new_session(self, session_name: str = None):
        """
        Create a new session.
        
        Args:
            session_name: Optional name for the session
        """
        timestamp = datetime.now()
        self.current_session_id = timestamp.strftime("%Y%m%d_%H%M%S")
        
        self.session_metadata = {
            'name': session_name or f"Chat {timestamp.strftime('%Y-%m-%d %H:%M')}",
            'created_at': timestamp.isoformat(),
            'last_accessed': timestamp.isoformat()
        }
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        session_path = self.get_session_path(session_id)
        
        if session_path.exists():
            try:
                session_path.unlink()
                return True
            except Exception:
                return False
        return False
    
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
        print("  /sessions           - List all saved sessions")
        print("  /new [name]         - Create a new session")
        print("  /load               - Load an existing session")
        print("  /delete             - Delete a session")
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
        print("  /sessions           - List all saved sessions")
        print("  /new [name]         - Create a new session with optional name")
        print("  /load               - Load an existing session")
        print("  /delete             - Delete a session")
        print("  /quit, /exit        - Exit the chat")
        print("\nAbout Temperature:")
        print("  • Lower (0.0-0.5): More focused and deterministic")
        print("  • Medium (0.5-1.0): Balanced creativity")
        print("  • Higher (1.0-2.0): More creative and random")
        print("\nAbout System Messages:")
        print("  System messages set the context and behavior of the AI.")
        print("  Example: /system You are a helpful coding assistant")
        print("\nAbout Sessions:")
        print("  Sessions are automatically saved after each message exchange.")
        print("  You can create, load, and manage multiple chat sessions.")
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
    
    def start_conversation(self, system_message: str = None, create_session: bool = True):
        """
        Start a new conversation.
        
        Args:
            system_message: Optional system message to set context
            create_session: Whether to create a new session
        """
        if system_message is None:
            system_message = "You are a helpful, friendly AI assistant."
        
        self.conversation = self.generator.create_conversation(
            system_message=system_message,
            model=self.current_model
        )
        
        if create_session and not self.current_session_id:
            self.create_new_session()
        
        print(f"✅ Conversation started with {self.current_model}")
        if system_message != "You are a helpful, friendly AI assistant.":
            print(f"📝 System: {system_message}")
        
        if self.current_session_id:
            session_name = self.session_metadata.get('name', 'Unknown')
            print(f"💾 Session: {session_name}")
        
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
    
    def show_sessions(self):
        """Display all available sessions."""
        sessions = self.list_sessions()
        
        print("\n💾 SAVED SESSIONS")
        print("-" * 80)
        
        if not sessions:
            print("(No saved sessions found)")
        else:
            for i, session in enumerate(sessions, 1):
                session_id = session['id']
                metadata = session['metadata']
                msg_count = session['message_count']
                
                name = metadata.get('name', 'Unnamed')
                created = metadata.get('created_at', 'Unknown')
                
                # Parse and format the created date
                try:
                    created_dt = datetime.fromisoformat(created)
                    created_str = created_dt.strftime('%Y-%m-%d %H:%M')
                except:
                    created_str = created
                
                current_marker = " (current)" if session_id == self.current_session_id else ""
                print(f"\n[{i}] {name}{current_marker}")
                print(f"    ID: {session_id}")
                print(f"    Created: {created_str}")
                print(f"    Messages: {msg_count}")
        
        print("\n" + "-" * 80)
        print()
    
    def select_session_to_load(self):
        """Interactive session loading."""
        sessions = self.list_sessions()
        
        if not sessions:
            print("❌ No saved sessions found.\n")
            return
        
        self.show_sessions()
        
        choice = input("Enter session number to load (or press Enter to cancel): ").strip()
        
        if not choice:
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                session_id = sessions[idx]['id']
                
                if self.load_session(session_id):
                    session_name = self.session_metadata.get('name', 'Unknown')
                    msg_count = len(self.conversation.get_history())
                    print(f"✅ Loaded session: {session_name}")
                    print(f"📊 Messages restored: {msg_count}\n")
                else:
                    print("❌ Failed to load session\n")
            else:
                print("❌ Invalid session number\n")
        except ValueError:
            print("❌ Please enter a valid number\n")
    
    def select_session_to_delete(self):
        """Interactive session deletion."""
        sessions = self.list_sessions()
        
        if not sessions:
            print("❌ No saved sessions found.\n")
            return
        
        self.show_sessions()
        
        choice = input("Enter session number to delete (or press Enter to cancel): ").strip()
        
        if not choice:
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                session_id = sessions[idx]['id']
                session_name = sessions[idx]['metadata'].get('name', 'Unknown')
                
                # Confirm deletion
                confirm = input(f"⚠️  Delete '{session_name}'? (yes/no): ").strip().lower()
                
                if confirm in ['yes', 'y']:
                    if self.delete_session(session_id):
                        print(f"✅ Session '{session_name}' deleted\n")
                        
                        # Clear current session if it was deleted
                        if self.current_session_id == session_id:
                            self.current_session_id = None
                            self.session_metadata = {}
                    else:
                        print("❌ Failed to delete session\n")
                else:
                    print("❌ Deletion cancelled\n")
            else:
                print("❌ Invalid session number\n")
        except ValueError:
            print("❌ Please enter a valid number\n")
    
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
        
        elif cmd == '/sessions':
            self.show_sessions()
        
        elif cmd == '/new':
            session_name = arg if arg else None
            self.current_session_id = None  # Clear current session
            self.session_metadata = {}
            self.start_conversation(create_session=True)
            if session_name:
                self.session_metadata['name'] = session_name
                self.save_session()
        
        elif cmd == '/load':
            self.select_session_to_load()
        
        elif cmd == '/delete':
            self.select_session_to_delete()
        
        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type /help for available commands\n")
        
        return True
    
    def startup_menu(self):
        """Show startup menu to select session."""
        sessions = self.list_sessions()
        
        print("\n🚀 STARTUP")
        print("-" * 80)
        print("What would you like to do?")
        print()
        print("  1. Start a new session")
        
        if sessions:
            print("  2. Continue from existing session")
            print()
            print(f"📊 You have {len(sessions)} saved session(s)")
        
        print()
        print("-" * 80)
        
        while True:
            choice = input("Enter choice (or press Enter for new session): ").strip()
            
            if not choice or choice == '1':
                # Start new session
                session_name = input("Session name (optional, press Enter to skip): ").strip()
                self.start_conversation(create_session=True)
                if session_name:
                    self.session_metadata['name'] = session_name
                    self.save_session()
                break
            
            elif choice == '2' and sessions:
                # Load existing session
                self.select_session_to_load()
                
                # If load was cancelled, ask again
                if not self.current_session_id:
                    print("\n⚠️  No session loaded. Please choose an option:\n")
                    continue
                break
            
            else:
                print("❌ Invalid choice. Please try again.\n")
    
    def run(self):
        """Run the interactive chat loop."""
        self.print_header()
        self.startup_menu()
        
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
                
                # Auto-save session after each exchange
                self.save_session()
                
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

