#!/usr/bin/env python3
"""
Test script for NamiBot
Demonstrates various Wikipedia document search functionalities and tests responses.
"""

from namibot import NamiBot
import time


def test_namibot_searches():
    """Test NamiBot with various Wikipedia document search queries."""
    print("🧪 Testing NamiBot")
    print("=" * 60)
    
    # Initialize NamiBot
    namibot = NamiBot("TestNamiBot")
    
    # Test cases for Wikipedia searches
    test_cases = [
        "What is artificial intelligence?",
        "Tell me about Albert Einstein",
        "Who is Marie Curie?",
        "Search for Python programming language",
        "What is quantum physics?",
        "Tell me about Leonardo da Vinci",
        "What is machine learning?",
        "Who is Isaac Newton?",
        "What is DNA?",
        "Tell me about the Great Wall of China",
        "What is blockchain technology?",
        "Who is Nikola Tesla?",
        "What is climate change?",
        "Tell me about the Renaissance",
        "What is virtual reality?"
    ]
    
    print("Running Wikipedia document search tests...\n")
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"Test {i}: '{test_input}'")
        print("-" * 50)
        
        response = namibot.get_response(test_input)
        print(f"Response: {response}")
        print("=" * 50)
        time.sleep(1)  # Delay between tests to be respectful to Wikipedia API
    
    # Test conversation history
    print("\n📝 Conversation History:")
    print("=" * 40)
    history = namibot.get_conversation_history()
    for entry in history:
        if "user" in entry:
            print(f"User: {entry['user']}")
        elif "bot" in entry:
            # Truncate long responses for display
            response = entry['bot']
            if len(response) > 100:
                response = response[:100] + "..."
            print(f"Bot: {response}")
        print(f"Time: {entry['timestamp'].strftime('%H:%M:%S')}")
        print()
    
    # Test statistics
    print("📊 NamiBot Statistics:")
    print("=" * 30)
    stats = namibot.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Test clearing history
    print("\n🗑️ Clearing conversation history...")
    result = namibot.clear_history()
    print(f"Result: {result}")
    print(f"History length after clearing: {len(namibot.get_conversation_history())}")


def test_basic_conversation():
    """Test basic conversation patterns."""
    print("\n💬 Testing Basic Conversation")
    print("=" * 40)
    
    namibot = NamiBot("ConvNamiBot")
    
    basic_tests = [
        "Hello",
        "What is your name?",
        "How are you?",
        "My name is Alice",
        "What time is it?",
        "Help",
        "Thank you",
        "Search count",
        "Goodbye"
    ]
    
    for test_input in basic_tests:
        print(f"Input: {test_input}")
        response = namibot.get_response(test_input)
        print(f"Response: {response}")
        print("-" * 30)


def test_error_handling():
    """Test error handling and edge cases."""
    print("\n⚠️ Testing Error Handling")
    print("=" * 40)
    
    namibot = NamiBot("ErrorNamiBot")
    
    edge_cases = [
        "",  # Empty input
        "   ",  # Whitespace only
        "xyz123",  # Non-existent topic
        "a" * 1000,  # Very long input
        "What is this very specific topic that probably doesn't exist on Wikipedia?",
    ]
    
    for test_input in edge_cases:
        print(f"Input: '{test_input}'")
        response = namibot.get_response(test_input)
        print(f"Response: {response}")
        print("-" * 30)


def test_research_commands():
    """Test research-specific commands."""
    print("\n🔬 Testing Research Commands")
    print("=" * 40)
    
    namibot = NamiBot("ResearchNamiBot")
    
    research_tests = [
        "Research quantum physics",
        "Search for information about space exploration",
        "Find documents about renewable energy",
        "Tell me about artificial intelligence",
        "What do you know about climate change?",
    ]
    
    for test_input in research_tests:
        print(f"Input: {test_input}")
        response = namibot.get_response(test_input)
        print(f"Response: {response}")
        print("-" * 30)


def interactive_demo():
    """Run an interactive demo of NamiBot."""
    print("\n🎮 Interactive NamiBot Demo")
    print("=" * 40)
    print("Type your questions and see how NamiBot searches Wikipedia documents!")
    print("Examples:")
    print("  - 'What is artificial intelligence?'")
    print("  - 'Tell me about Albert Einstein'")
    print("  - 'Research quantum physics'")
    print("Type 'quit' to exit the demo.\n")
    
    namibot = NamiBot("DemoNamiBot")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print(f"{namibot.name}: Goodbye! Thanks for testing NamiBot!")
            break
        
        if user_input.lower() == 'stats':
            stats = namibot.get_stats()
            print(f"\n📊 NamiBot Statistics:")
            print(f"   Total searches: {stats['total_searches']}")
            print(f"   Conversation length: {stats['conversation_length']}")
            print(f"   Bot name: {stats['bot_name']}")
            print(f"   User name: {stats['user_name']}")
            continue
        
        if user_input:
            response = namibot.get_response(user_input)
            print(f"{namibot.name}: {response}\n")


def main():
    """Main function to run tests and demo."""
    print("🤖 NamiBot - Test Suite")
    print("=" * 60)
    
    # Test basic conversation first
    test_basic_conversation()
    
    # Test research commands
    test_research_commands()
    
    # Test NamiBot searches
    test_namibot_searches()
    
    # Test error handling
    test_error_handling()
    
    # Ask if user wants interactive demo
    print("\n" + "=" * 60)
    choice = input("Would you like to try the interactive NamiBot demo? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        interactive_demo()
    else:
        print("Thanks for testing! Run 'python namibot.py' for the full console version.")
        print("Or run 'python gui_namibot.py' for the GUI version.")


if __name__ == "__main__":
    main() 