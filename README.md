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

## Setup

1. Install dependencies using Magic (from Modular):
   ```bash
   magic install
   ```

2. Create a `.env` file with your Anthropic API key:
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
magic run python cli.py "What is the capital of France?"

# Stream the response
magic run python cli.py -s "Tell me a story"

# Control temperature
magic run python cli.py -t 0.2 "Solve this math problem"

# Read prompt from stdin
echo "What is the meaning of life?" | magic run python cli.py

# Interactive mode (press Ctrl+D to submit)
magic run python cli.py
```

CLI Options:
- `-s, --stream`: Stream the response in real-time
- `-t, --temperature`: Set response temperature (0.0 to 1.0, default: 1.0)

## Testing

The project includes a comprehensive test suite:

```bash
# Run all tests
magic run pytest

# Run tests with verbose output
magic run pytest -v

# Run a specific test file
magic run pytest tests/test_anthropic_client.py
```

## Dependencies

- anthropic - Core API client library (latest version)
- python-dotenv - Environment variable management
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