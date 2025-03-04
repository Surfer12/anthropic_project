# Anthropic API Client

This project provides a Python client and CLI for interacting with Anthropic's Claude models, specifically optimized for Claude 3.7 Sonnet.

## Features

- **Advanced Model Support**: Uses Claude 3.7 Sonnet model with 128k context window
- **Enhanced Capabilities**:
  - Thinking capability enabled with 128k token budget
  - Temperature control for response randomness
  - Streaming support for real-time responses
- **Multiple Interfaces**:
  - Python library for programmatic usage
  - Command-line interface (CLI) for direct interaction
- **Developer Friendly**:
  - Type hints for better IDE support
  - Comprehensive error handling
  - Environment-based configuration

## Project Structure

```
anthropic_client/
├── anthropic_client/
│   ├── __init__.py
│   ├── client.py    # Core client implementation
│   └── cli.py       # Command-line interface
├── tests/
│   └── test_*.py    # Test files
├── README.md
├── setup.py         # Package configuration
└── requirements.txt # Development dependencies
```

## Installation

### Using Magic (Recommended)

1. Install dependencies using Magic (from Modular):
   ```bash
   magic install
   ```

2. Install the package in development mode:
   ```bash
   magic run pip install -e .
   ```

### Using pip

```bash
pip install .
```

### Environment Setup

Create a `.env` file with your Anthropic API key:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## Usage

### Python Library

```python
from anthropic_client import AnthropicClient

# Initialize the client
client = AnthropicClient()

# Get a complete response
response = client.get_response("Hello, Claude!")
print(response)

# Stream a response
for chunk in client.get_response("Tell me a story", stream=True):
    print(chunk, end="", flush=True)

# Control response randomness
focused_response = client.get_response("Solve this math problem", temperature=0.2)
```

### Command Line Interface

The CLI supports both direct prompts and stdin input:

```bash
# Direct prompt
claude "What is the capital of France?"

# Stream the response
claude -s "Tell me a story"

# Control temperature
claude -t 0.2 "Solve this math problem"

# Read prompt from stdin
echo "What is the meaning of life?" | claude

# Interactive mode (press Ctrl+D to submit)
claude
```

CLI Options:
- `-s, --stream`: Stream the response in real-time
- `-t, --temperature`: Set response temperature (0.0 to 1.0, default: 1.0)

## Development

### Testing

The project includes a comprehensive test suite:

```bash
# Run all tests
magic run pytest

# Run tests with verbose output
magic run pytest -v

# Run a specific test file
magic run pytest tests/test_anthropic_client.py
```

### Dependencies

- anthropic (>=0.18.1) - Core API client library
- python-dotenv (>=1.0.0) - Environment variable management
- pytest - Testing framework
- flake8 - Code linting
- mypy - Type checking

## Error Handling

The client handles common errors:
- Missing API key
- Network issues
- Invalid prompts
- Keyboard interrupts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request