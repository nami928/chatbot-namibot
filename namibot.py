#!/usr/bin/env python3
"""
NamiBot - Wikipedia Document Chatbot
A smart chatbot that can search and retrieve information from Wikipedia documents.
"""

import re
import random
import time
from datetime import datetime
import wikipediaapi
import requests
from urllib.parse import quote


class NamiBot:
    def __init__(self, name="NamiBot", language="en"):
        self.name = name
        self.user_name = "User"
        self.conversation_history = []
        self.language = language
        self.search_count = 0
        
        # Initialize Wikipedia API
        try:
            self.wiki = wikipediaapi.Wikipedia(
                language=language,
                user_agent="NamiBot/1.0 (https://github.com/user/chatbot-namibot; user@example.com)"
            )
            self.wiki_available = True
            print(f"✅ {self.name} initialized successfully with Wikipedia API access!")
        except Exception as e:
            print(f"⚠️ Warning: Wikipedia API not available: {e}")
            self.wiki_available = False
        
        # Define response patterns
        self.patterns = {
            r'\b(hi|hello|hey|greetings)\b': [
                f"Hello! I'm {self.name}, your Wikipedia research assistant! What would you like to learn about today?",
                f"Hi there! I'm {self.name}. I can search Wikipedia documents for you!",
                f"Hello! I'm {self.name}! Ask me anything and I'll find the information in Wikipedia documents!"
            ],
            r'\b(how are you|how do you do)\b': [
                f"I'm doing great! Ready to search Wikipedia documents for you, {self.user_name}!",
                "I'm functioning perfectly! What topic would you like me to research?",
                "All systems operational! I'm ready to help you find information in Wikipedia documents!"
            ],
            r'\b(what is your name|who are you)\b': [
                f"My name is {self.name}! I'm a Wikipedia document research assistant.",
                f"I'm {self.name}, your friendly Wikipedia document explorer.",
                f"You can call me {self.name}! I help people find information in Wikipedia documents."
            ],
            r'\b(bye|goodbye|see you|exit|quit)\b': [
                f"Goodbye! It was nice helping you research Wikipedia documents, {self.user_name}!",
                "See you later! Feel free to come back for more Wikipedia knowledge!",
                "Take care! Wikipedia documents are always here when you need information!"
            ],
            r'\b(thank you|thanks)\b': [
                "You're welcome! Wikipedia documents have so much knowledge to share.",
                "My pleasure! I love helping people discover information in Wikipedia documents.",
                "Glad I could help! Wikipedia is an amazing resource for learning."
            ],
            r'\b(what time|current time)\b': [
                f"The current time is {datetime.now().strftime('%H:%M:%S')}",
                f"It's {datetime.now().strftime('%I:%M %p')} right now",
                f"Current time: {datetime.now().strftime('%H:%M:%S')}"
            ],
            r'\b(what date|today|date)\b': [
                f"Today is {datetime.now().strftime('%A, %B %d, %Y')}",
                f"The date is {datetime.now().strftime('%m/%d/%Y')}",
                f"Today: {datetime.now().strftime('%B %d, %Y')}"
            ],
            r'\b(help|what can you do)\b': [
                "I can search Wikipedia documents for any topic! Just ask me about anything - people, places, events, concepts, etc.",
                "I'm a Wikipedia document chatbot! Ask me about any topic and I'll find the information for you.",
                "I can help you learn about anything by searching Wikipedia documents. Just ask me a question!"
            ],
            r'\b(wikipedia|wiki)\b': [
                "Wikipedia is a free online encyclopedia with millions of documents! I can search it for you.",
                "Wikipedia is one of the largest knowledge bases in the world. What would you like to know?",
                "Wikipedia documents have information on almost everything! What topic interests you?"
            ],
            r'\b(search count|how many searches)\b': [
                f"I've performed {self.search_count} Wikipedia searches so far in this session!",
                f"Current search count: {self.search_count} Wikipedia document searches.",
                f"I've searched Wikipedia documents {self.search_count} times for you!"
            ]
        }
        
        # Default responses for unrecognized input
        self.default_responses = [
            "I'm not sure I understand. Could you ask me about a specific topic to search in Wikipedia documents?",
            "Interesting! Let me search Wikipedia documents for that. Could you be more specific?",
            "I'm here to help you find information in Wikipedia documents. What would you like to learn about?",
            "That's an interesting question! Let me search Wikipedia documents for you. Could you rephrase it?",
            "I can search Wikipedia documents for almost anything! What topic would you like to explore?"
        ]
    
    def search_wikipedia_documents(self, query, max_results=3):
        """Search Wikipedia documents for a given query."""
        if not self.wiki_available:
            return None, "Sorry, Wikipedia API is not available right now."
        
        try:
            # Increment search count
            self.search_count += 1
            
            # Try to get the page directly
            page = self.wiki.page(query)
            
            if page.exists():
                # Extract summary (first 600 characters for more detailed responses)
                summary = page.summary[:600]
                if len(page.summary) > 600:
                    summary += "..."
                
                return {
                    'title': page.title,
                    'summary': summary,
                    'url': page.fullurl,
                    'exists': True,
                    'search_count': self.search_count
                }, None
            else:
                # If direct page doesn't exist, try some common variations
                variations = [
                    query.title(),
                    query.capitalize(),
                    query.replace(" ", "_"),
                    query.replace(" ", " ").title(),
                    query.lower().title()
                ]
                
                for variation in variations:
                    if variation != query:
                        page = self.wiki.page(variation)
                        if page.exists():
                            summary = page.summary[:600]
                            if len(page.summary) > 600:
                                summary += "..."
                            
                            return {
                                'title': page.title,
                                'summary': summary,
                                'url': page.fullurl,
                                'exists': True,
                                'search_count': self.search_count
                            }, None
                
                # If no variations work, provide a helpful message
                return None, f"I couldn't find any Wikipedia documents about '{query}'. Try being more specific or check the spelling."
        
        except Exception as e:
            return None, f"Sorry, there was an error searching Wikipedia documents: {str(e)}"
    
    def get_response(self, user_input):
        """Generate a response based on user input."""
        # Store the conversation
        self.conversation_history.append({"user": user_input, "timestamp": datetime.now()})
        
        # Convert to lowercase for pattern matching
        user_input_lower = user_input.lower().strip()
        
        # Check for name setting
        if "my name is" in user_input_lower or "i'm" in user_input_lower:
            name_match = re.search(r'(?:my name is|i\'m)\s+(\w+)', user_input_lower)
            if name_match:
                self.user_name = name_match.group(1).title()
                return f"Nice to meet you, {self.user_name}! I'll remember your name."
        
        # Check for Wikipedia search patterns
        search_patterns = [
            r'(?:what is|who is|tell me about|search for|find information about|what do you know about)\s+(.+)',
            r'(?:can you tell me|do you know|i want to know about)\s+(.+)',
            r'(.+)\s+(?:on wikipedia|in wikipedia|from wikipedia)',
            r'(?:explain|describe|research)\s+(.+)',
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                search_query = match.group(1).strip()
                # Remove question marks and other punctuation
                search_query = re.sub(r'[?!.,;:]', '', search_query).strip()
                if search_query:
                    return self.handle_wikipedia_search(search_query)
        
        # Check if the input looks like a direct question (starts with what, who, when, where, how, why)
        question_words = ['what', 'who', 'when', 'where', 'how', 'why']
        if any(user_input_lower.startswith(word) for word in question_words):
            # Extract the topic from the question
            words = user_input_lower.split()
            if len(words) > 2:  # Skip question word and common words
                # Remove common question words and articles
                common_words = {'what', 'who', 'when', 'where', 'how', 'why', 'is', 'are', 'was', 'were', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
                topic_words = [word for word in words[1:] if word not in common_words]
                if topic_words:
                    search_query = ' '.join(topic_words[:4])  # Take first 4 words as topic
                    # Remove question marks and other punctuation
                    search_query = re.sub(r'[?!.,;:]', '', search_query).strip()
                    return self.handle_wikipedia_search(search_query)
        
        # Check patterns for matches
        for pattern, responses in self.patterns.items():
            if re.search(pattern, user_input_lower):
                response = random.choice(responses)
                self.conversation_history.append({"bot": response, "timestamp": datetime.now()})
                return response
        
        # If no pattern matches, return a default response
        response = random.choice(self.default_responses)
        self.conversation_history.append({"bot": response, "timestamp": datetime.now()})
        return response
    
    def handle_wikipedia_search(self, query):
        """Handle Wikipedia search and format response."""
        result, error = self.search_wikipedia_documents(query)
        
        if error:
            response = error
        elif result and result.get('exists'):
            # Found a page
            title = result['title']
            summary = result['summary']
            url = result['url']
            search_count = result['search_count']
            
            response = f"📚 **{title}**\n\n{summary}\n\n🔗 Read full document: {url}\n\n📊 Search #{search_count} in this session"
        else:
            response = f"I couldn't find Wikipedia documents about '{query}'. Try rephrasing your question or asking about a different topic."
        
        self.conversation_history.append({"bot": response, "timestamp": datetime.now()})
        return response
    
    def get_conversation_history(self):
        """Return the conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.search_count = 0
        return "Conversation history and search count cleared!"
    
    def get_stats(self):
        """Get bot statistics."""
        return {
            'total_searches': self.search_count,
            'conversation_length': len(self.conversation_history),
            'bot_name': self.name,
            'user_name': self.user_name
        }


def main():
    """Main function to run NamiBot in console mode."""
    print("=" * 70)
    print("🤖 NamiBot - Wikipedia Document Assistant")
    print("=" * 70)
    print("I can search Wikipedia documents for information on any topic!")
    print("Examples:")
    print("  - 'What is artificial intelligence?'")
    print("  - 'Tell me about Albert Einstein'")
    print("  - 'Search for Python programming language'")
    print("  - 'Who is Marie Curie?'")
    print("  - 'Research quantum physics'")
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'help' to see what I can do")
    print("Type 'stats' to see search statistics")
    print("=" * 70)
    
    namibot = NamiBot("NamiBot")
    
    while True:
        try:
            user_input = input(f"\n{namibot.user_name}: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n{namibot.name}: {namibot.get_response(user_input)}")
                break
            
            if user_input.lower() == 'stats':
                stats = namibot.get_stats()
                print(f"\n📊 NamiBot Statistics:")
                print(f"   Total searches: {stats['total_searches']}")
                print(f"   Conversation length: {stats['conversation_length']}")
                print(f"   Bot name: {stats['bot_name']}")
                print(f"   User name: {stats['user_name']}")
                continue
            
            response = namibot.get_response(user_input)
            print(f"\n{namibot.name}: {response}")
            
        except KeyboardInterrupt:
            print(f"\n\n{namibot.name}: Goodbye! Thanks for using NamiBot!")
            break
        except EOFError:
            print(f"\n\n{namibot.name}: Goodbye! Thanks for using NamiBot!")
            break


if __name__ == "__main__":
    main() 