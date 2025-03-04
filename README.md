# Anthropic API Client

This project provides a Python client and CLI for interacting with Anthropic's Claude models, specifically optimized for Claude 3.7 Sonnet.

## Features

- **Advanced Model Support**: Uses Claude 3.7 Sonnet model with 128k context window
- **Enhanced Capabilities**:
  - Thinking capability enabled with 128k token budget
  - Temperature control for response randomness (0.0 to 1.0)
  - Streaming support for real-time responses
  - Comprehensive error handling and retries
- **Multiple Interfaces**:
  - Python library for programmatic usage
  - Command-line interface (CLI) for direct interaction
- **Developer Friendly**:
  - Type hints for better IDE support
  - Comprehensive error handling
  - Environment-based configuration
  - Extensive test coverage
  - Detailed logging

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
claudethink "What is the capital of France?"

# Stream the response
claudethink -s "Tell me a story"

# Control temperature
claudethink -t 0.2 "Solve this math problem"

# Read prompt from stdin
echo "What is the meaning of life?" | claudethink

# Interactive mode (press Ctrl+D to submit)
claudethink
```

CLI Options:
- `-s, --stream`: Stream the response in real-time
- `-t, --temperature`: Set response temperature (0.0 to 1.0, default: 1.0)

## Development

### Testing

The project includes a comprehensive test suite covering all major functionality:

```bash
# Run all tests
magic run pytest

# Run tests with coverage report
magic run pytest --cov=anthropic_client tests/

# Run specific test categories
magic run pytest tests/test_anthropic_client.py  # Core client tests
magic run pytest tests/test_cli.py               # CLI tests
magic run pytest tests/test_integration.py       # Integration tests
magic run pytest tests/test_environment.py       # Environment setup tests
```

### Test Coverage

The test suite includes:
- Unit tests for core functionality
- Integration tests with the Anthropic API
- CLI command testing
- Error handling and edge cases
- Environment configuration testing
- Streaming response testing
- Mock tests for API interactions

### Error Handling

The client handles various error scenarios:

1. **API Errors**:
   - Authentication failures
   - Rate limiting
   - Invalid requests
   - Network timeouts
   - Streaming errors

2. **Configuration Errors**:
   - Missing API keys
   - Invalid environment setup
   - Invalid parameter values

3. **Runtime Errors**:
   - Connection issues
   - Timeout handling
   - Stream interruptions
   - Resource cleanup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass:
   ```bash
   magic run pytest
   magic run flake8
   magic run mypy .
   ```
5. Submit a pull request

## Logging

The client includes detailed logging for debugging and monitoring:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

client = AnthropicClient()
```

Log levels:
- DEBUG: API request/response details
- INFO: General operation information
- WARNING: Non-critical issues
- ERROR: Critical failures

## Security

- API keys are loaded from environment variables only
- Sensitive data is never logged
- All network requests use HTTPS
- Rate limiting is respected
- Proper error handling prevents data leaks

## License

This project is licensed under the MIT License - see the LICENSE file for details.