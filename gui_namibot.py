#!/usr/bin/env python3
"""
GUI NamiBot Implementation
A graphical interface for NamiBot with enhanced display features for Wikipedia documents.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from namibot import NamiBot
import threading
import time
import webbrowser
import re


class NamiBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NamiBot - Wikipedia Document Assistant")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize NamiBot
        self.namibot = NamiBot("NamiBot")
        
        # Create GUI elements
        self.create_widgets()
        
        # Bind Enter key to send message
        self.root.bind('<Return>', self.send_message)
        
        # Welcome message
        self.display_bot_message("Hello! I'm NamiBot, your Wikipedia document assistant. Ask me about any topic!")
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=90,
            height=35,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Bind click events for URLs
        self.chat_display.tag_bind("url", "<Button-1>", self.open_url)
        self.chat_display.tag_bind("url", "<Enter>", self.on_url_enter)
        self.chat_display.tag_bind("url", "<Leave>", self.on_url_leave)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Message input
        self.message_input = ttk.Entry(
            input_frame,
            font=("Arial", 10),
            width=70
        )
        self.message_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Clear chat button
        self.clear_button = ttk.Button(
            control_frame,
            text="Clear Chat",
            command=self.clear_chat
        )
        self.clear_button.grid(row=0, column=0, padx=(0, 10))
        
        # Stats button
        self.stats_button = ttk.Button(
            control_frame,
            text="Statistics",
            command=self.show_stats
        )
        self.stats_button.grid(row=0, column=1, padx=(0, 10))
        
        # Help button
        self.help_button = ttk.Button(
            control_frame,
            text="Help",
            command=self.show_help
        )
        self.help_button.grid(row=0, column=2, padx=(0, 10))
        
        # Examples button
        self.examples_button = ttk.Button(
            control_frame,
            text="Examples",
            command=self.show_examples
        )
        self.examples_button.grid(row=0, column=3, padx=(0, 10))
        
        # Exit button
        self.exit_button = ttk.Button(
            control_frame,
            text="Exit",
            command=self.exit_app
        )
        self.exit_button.grid(row=0, column=4)
    
    def display_user_message(self, message):
        """Display a user message in the chat area."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {message}\n", "user")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def display_bot_message(self, message):
        """Display a bot message in the chat area with URL detection."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Insert the message
        self.chat_display.insert(tk.END, f"{self.namibot.name}: ", "bot")
        
        # Check if message contains URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message)
        
        if urls:
            # Split message by URLs and insert with formatting
            parts = re.split(url_pattern, message)
            for i, part in enumerate(parts):
                if part:
                    self.chat_display.insert(tk.END, part)
                if i < len(urls):
                    url = urls[i]
                    self.chat_display.insert(tk.END, url, "url")
        else:
            self.chat_display.insert(tk.END, message)
        
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def open_url(self, event):
        """Open URL in default browser."""
        try:
            # Get the URL from the clicked tag
            index = self.chat_display.index(f"@{event.x},{event.y}")
            line_start = self.chat_display.index(f"{index} linestart")
            line_end = self.chat_display.index(f"{index} lineend")
            line = self.chat_display.get(line_start, line_end)
            
            # Extract URL from the line
            url_pattern = r'https?://[^\s]+'
            urls = re.findall(url_pattern, line)
            if urls:
                webbrowser.open(urls[0])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {e}")
    
    def on_url_enter(self, event):
        """Change cursor when hovering over URL."""
        self.chat_display.config(cursor="hand2")
    
    def on_url_leave(self, event):
        """Reset cursor when leaving URL."""
        self.chat_display.config(cursor="")
    
    def send_message(self, event=None):
        """Send a message and get bot response."""
        message = self.message_input.get().strip()
        if not message:
            return
        
        # Clear input field
        self.message_input.delete(0, tk.END)
        
        # Display user message
        self.display_user_message(message)
        
        # Disable send button temporarily
        self.send_button.config(state=tk.DISABLED)
        
        # Get bot response in a separate thread to avoid GUI freezing
        threading.Thread(target=self.get_bot_response, args=(message,), daemon=True).start()
    
    def get_bot_response(self, message):
        """Get bot response and display it."""
        # Simulate typing delay for more natural feel
        time.sleep(0.5)
        
        # Get response from NamiBot
        response = self.namibot.get_response(message)
        
        # Display response in main thread
        self.root.after(0, lambda: self.display_bot_response(response))
    
    def display_bot_response(self, response):
        """Display bot response and re-enable send button."""
        self.display_bot_message(response)
        self.send_button.config(state=tk.NORMAL)
        self.message_input.focus()
    
    def clear_chat(self):
        """Clear the chat display and conversation history."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Clear NamiBot history
        self.namibot.clear_history()
        
        # Display welcome message again
        self.display_bot_message("Hello! I'm NamiBot, your Wikipedia document assistant. Ask me about any topic!")
    
    def show_stats(self):
        """Show NamiBot statistics."""
        stats = self.namibot.get_stats()
        stats_text = f"""
📊 NamiBot Statistics

Total Wikipedia searches: {stats['total_searches']}
Conversation length: {stats['conversation_length']} messages
Bot name: {stats['bot_name']}
User name: {stats['user_name']}

Session started: {time.strftime('%Y-%m-%d %H:%M:%S')}
        """
        messagebox.showinfo("NamiBot Statistics", stats_text.strip())
    
    def show_help(self):
        """Show help information."""
        help_text = """
🤖 NamiBot Help

I can search Wikipedia documents for information on any topic!

How to use:
• Ask questions like "What is artificial intelligence?"
• Use phrases like "Tell me about Albert Einstein"
• Search for topics with "Search for Python programming"
• Ask "Who is Marie Curie?" or "What is quantum physics?"
• Use "Research quantum physics" for document searches

Features:
• Real-time Wikipedia document searches
• Clickable links to full articles
• Conversation history
• Search statistics
• Smart topic detection

Commands:
• Type your message and press Enter or click Send
• Use "Clear Chat" to start a new conversation
• Click "Statistics" to see search count and session info
• Click "Examples" to see sample questions
• Type "stats" to see search statistics
• Click on any URL to open the full Wikipedia document

Just ask me anything and I'll find the information for you!
        """
        messagebox.showinfo("Help", help_text.strip())
    
    def show_examples(self):
        """Show example questions."""
        examples_text = """
📚 Example Questions for NamiBot

People:
• "Who is Albert Einstein?"
• "Tell me about Marie Curie"
• "What do you know about Leonardo da Vinci?"

Concepts:
• "What is artificial intelligence?"
• "Tell me about quantum physics"
• "What is machine learning?"

Places:
• "Tell me about Paris"
• "What is the Great Wall of China?"
• "Search for information about Tokyo"

Technology:
• "What is Python programming?"
• "Tell me about blockchain"
• "What is virtual reality?"

History:
• "What was World War II?"
• "Tell me about the Renaissance"
• "What is the Industrial Revolution?"

Science:
• "What is DNA?"
• "Tell me about black holes"
• "What is climate change?"

Research Commands:
• "Research quantum physics"
• "Search for information about space exploration"
• "Find documents about renewable energy"

Just copy any of these questions or ask your own!
        """
        messagebox.showinfo("Examples", examples_text.strip())
    
    def exit_app(self):
        """Exit the application."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()


def main():
    """Main function to run the GUI NamiBot."""
    root = tk.Tk()
    
    # Configure text tags for styling
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    app = NamiBotGUI(root)
    
    # Configure text tags for chat display
    app.chat_display.tag_configure("user", foreground="blue", font=("Arial", 10, "bold"))
    app.chat_display.tag_configure("bot", foreground="green", font=("Arial", 10, "bold"))
    app.chat_display.tag_configure("url", foreground="purple", underline=True, font=("Arial", 10, "bold"))
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main() 