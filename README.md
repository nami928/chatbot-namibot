# NamiBot

A smart chatbot that can search and retrieve information from Wikipedia documents using the Wikipedia API.

## Features

- 🔍 **Wikipedia Document Integration** - Real-time searches using Wikipedia API
- 📚 **Smart Content Retrieval** - Gets detailed summaries and full article links
- 💬 **Intelligent Conversation** - Understands various question formats and research commands
- 🖥️ **GUI Interface** - Modern tkinter-based interface with clickable links
- 📝 **Console Interface** - Simple command-line interface
- 🧪 **Comprehensive Testing** - Test suite with various search scenarios
- 📖 **Document Summaries** - Provides detailed summaries with links to full articles
- 🔗 **Clickable URLs** - Direct links to Wikipedia documents (GUI version)
- 📊 **Search Statistics** - Track search count and conversation history
- 🔬 **Research Commands** - Special commands for document research

## Installation

### Option 1: Using Conda (Recommended)

1. **Clone or download the project**
   ```bash
   cd chatbot-namibot
   ```

2. **Create and activate conda environment**
   ```bash
   conda create -n namibot python=3.11 -y
   conda activate namibot
   ```

3. **Install dependencies**
   ```bash
   pip install wikipedia-api requests
   ```

### Option 2: Using pip directly

1. **Clone or download the project**
   ```bash
   cd chatbot-namibot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run NamiBot**

   **Quick Start (Launcher):**
   ```bash
   # Make sure conda environment is activated
   conda activate namibot
   python run.py
   ```

   **Console version:**
   ```bash
   conda activate namibot
   python namibot.py
   ```

   **GUI version:**
   ```bash
   conda activate namibot
   python gui_namibot.py
   ```

   **Test suite:**
   ```bash
   conda activate namibot
   python test_namibot.py
   ```

## Usage

### Console Interface

Run `conda activate namibot && python namibot.py` and start asking questions! NamiBot will search Wikipedia documents for:

- **People**: "Who is Albert Einstein?", "Tell me about Marie Curie"
- **Concepts**: "What is artificial intelligence?", "What is quantum physics?"
- **Places**: "Tell me about Paris", "What is the Great Wall of China?"
- **Technology**: "What is Python programming?", "Tell me about blockchain"
- **History**: "What was World War II?", "Tell me about the Renaissance"
- **Science**: "What is DNA?", "Tell me about black holes"
- **Research**: "Research quantum physics", "Search for information about space exploration"

### GUI Interface

Run `conda activate namibot && python gui_namibot.py` for a graphical interface with:

- **Chat display** - Scrollable conversation area with formatted text
- **Input field** - Type your questions
- **Send button** - Send messages with a click
- **Clickable links** - Click on URLs to open Wikipedia documents
- **Statistics button** - View search count and session information
- **Clear chat** - Start a new conversation
- **Help & Examples** - Built-in help system with example questions
- **Exit button** - Close the application

### Question Formats

NamiBot understands various ways to ask questions:

- **Direct questions**: "What is artificial intelligence?"
- **Tell me about**: "Tell me about Albert Einstein"
- **Search requests**: "Search for Python programming language"
- **Who is**: "Who is Marie Curie?"
- **What is**: "What is quantum physics?"
- **Research commands**: "Research quantum physics", "Find documents about renewable energy"

### Special Commands

- **`stats`** - Show search statistics and session information
- **`help`** - Display help information
- **`quit`/`exit`/`bye`** - End the conversation

## Project Structure

```
chatbot-namibot/
├── namibot.py          # Main NamiBot class and console interface
├── gui_namibot.py      # GUI interface using tkinter
├── test_namibot.py     # Test suite and demo
├── run.py             # Launcher script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## How It Works

NamiBot uses a **multi-layered approach**:

1. **Input Processing**: Analyzes user input for search patterns
2. **Question Detection**: Identifies various question formats and research commands
3. **Wikipedia API**: Searches Wikipedia using the `wikipedia-api` library
4. **Content Extraction**: Retrieves detailed article summaries and URLs
5. **Response Formatting**: Formats responses with links and search statistics
6. **Fallback Handling**: Provides helpful suggestions for similar topics

### Wikipedia API Integration

```python
# Initialize Wikipedia API
self.wiki = wikipediaapi.Wikipedia(
    language=language,
    user_agent="NamiBot/1.0 (https://github.com/user/chatbot-namibot; user@example.com)"
)

# Search for pages
page = self.wiki.page(query)
if page.exists():
    summary = page.summary[:600]  # Get first 600 characters
    url = page.fullurl           # Get full article URL
```

### Smart Question Detection

NamiBot recognizes multiple question patterns:

```python
search_patterns = [
    r'(?:what is|who is|tell me about|search for|research)\s+(.+)',
    r'(?:can you tell me|do you know|find documents about)\s+(.+)',
    r'(.+)\s+(?:on wikipedia|in wikipedia|from wikipedia)',
]
```

## Dependencies

- **wikipedia-api**: Official Wikipedia API wrapper
- **requests**: HTTP library for web requests
- **tkinter**: GUI framework (usually included with Python)
- **Optional**: nltk, textblob for advanced text processing

## Example Conversations

```
User: What is artificial intelligence?
NamiBot: 📚 **Artificial intelligence**

Artificial intelligence (AI) is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals...

🔗 Read full document: https://en.wikipedia.org/wiki/Artificial_intelligence

📊 Search #1 in this session

User: Research quantum physics
NamiBot: 📚 **Quantum mechanics**

Quantum mechanics is a fundamental theory in physics that describes the behavior of matter and energy at the atomic and subatomic scales. It is the foundation of all quantum physics including quantum chemistry, quantum field theory, quantum technology, and quantum information science...

🔗 Read full document: https://en.wikipedia.org/wiki/Quantum_mechanics

📊 Search #2 in this session
```

## Customization

### Adding New Search Patterns

To add new question patterns, modify the `search_patterns` list in `namibot.py`:

```python
search_patterns = [
    # ... existing patterns ...
    r'(?:explain|describe|investigate)\s+(.+)',
    r'(.+)\s+(?:explanation|description|investigation)',
]
```

### Changing Language

Modify the language when initializing:

```python
namibot = NamiBot("NamiBot", language="es")  # Spanish
namibot = NamiBot("NamiBot", language="fr")  # French
```

### Customizing Response Format

Modify the `handle_wikipedia_search` method to change response formatting:

```python
response = f"📖 **{title}**\n\n{summary}\n\n🌐 Full document: {url}\n\n📊 Search #{search_count}"
```

## Error Handling

NamiBot includes robust error handling:

- **API Unavailable**: Graceful fallback when Wikipedia API is down
- **No Results**: Provides helpful suggestions for similar topics
- **Network Issues**: Handles connection problems gracefully
- **Invalid Input**: Responds appropriately to malformed queries

## Future Enhancements

Potential improvements:

- 🌍 **Multi-language Support** - Support for multiple Wikipedia languages
- 📊 **Rich Media** - Display images and infoboxes
- 🔍 **Advanced Search** - Fuzzy matching and semantic search
- 💾 **Search History** - Save and recall previous searches
- 🎨 **Custom Themes** - Different GUI themes and styles
- 📱 **Web Interface** - Flask/Django web application
- 🤖 **Voice Interface** - Speech-to-text and text-to-speech
- 📈 **Analytics Dashboard** - Detailed search analytics and insights

## Contributing

Feel free to:

1. Add new search patterns and research commands
2. Improve the GUI design and user experience
3. Add support for more Wikipedia features
4. Implement additional language support
5. Add more test cases and edge case handling
6. Enhance the statistics and analytics features

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure to install dependencies with `pip install -r requirements.txt`
2. **Wikipedia API Error**: Check internet connection and Wikipedia API status
3. **GUI Not Working**: Ensure tkinter is available (usually included with Python)
4. **Slow Responses**: Wikipedia API may be slow during peak times

### Getting Help

- Run the test suite: `conda activate namibot && python test_namibot.py`
- Check the console for error messages
- Ensure all dependencies are installed
- Verify internet connection
- Use the `stats` command to check search count

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Wikipedia API** - For providing access to Wikipedia content
- **wikipedia-api library** - Python wrapper for Wikipedia API
- **Wikipedia contributors** - For creating the vast knowledge base

---

**Happy Researching! 🤖📚🔬**