# Anthropic API Client

This project provides a Python client and CLI for interacting with Anthropic's Claude models, specifically optimized for Claude 3.7 Sonnet.

## Features

- **Advanced Model Support**: Uses Claude 3.7 Sonnet model with 128k context window
- **Enhanced Capabilities**:
  - Thinking capability enabled with 128k token budget
  - Temperature control for response randomness (0.0 to 1.0)
  - Streaming support for real-time responses
  - Comprehensive error handling and retries
- **Multiple Implementations**:
  - Python library for programmatic usage
  - Command-line interface (CLI) for direct interaction
  - Mojo implementation for better performance
- **Developer Friendly**:
  - Type hints for better IDE support
  - Comprehensive error handling
  - Environment-based configuration
  - Extensive test coverage
  - Detailed logging

## Project Structure

```
anthropic_client/
├── anthropic_client/       # Python implementation
│   ├── __init__.py
│   ├── client.py           # Core client implementation
│   └── cli.py              # Command-line interface
├── anthropic_client_mojo/  # Mojo implementation
│   ├── __init__.py
│   ├── client.mojo         # Mojo client
│   ├── cli.mojo            # Mojo CLI
│   └── python_cli.py       # Python-to-Mojo bridge
├── bin/                    # CLI executables (after installation)
├── tests/                  # Test files
├── README.md
├── pixi.toml               # Magic/Pixi package configuration
├── magic.lock              # Magic lock file
└── setup.py                # Python package configuration
```

## Installation

### Using Magic Toolchain (Recommended)

The project uses Modular's Magic toolchain for dependency management and running both Python and Mojo code.

1. **Install Magic** (if not already installed):
   ```bash
   curl https://get.modular.com | sh
   ```

2. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/anthropic_client.git
   cd anthropic_client
   ```

3. **Install dependencies with Magic**:
   ```bash
   magic install
   ```

4. **Install the package in development mode**:
   ```bash
   magic run pixi task dev-install
   ```

5. **Install the CLI tools**:
   ```bash
   magic run pixi task install-cli
   ```

### Using pip (Python-only features)

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
# Direct prompt with Python implementation
claudethink "What is the capital of France?"

# Direct prompt with Mojo implementation (better performance)
claudethinkmojo "What is the capital of France?"

# Stream the response
claudethinkstream "Tell me a story"

# Control temperature
claudethinkfast "Solve this math problem"

# Use a specific model
claudethink -m claude-3-opus-20240229 "Complex analysis task"

# Save response to file
claudethinkfile response.txt "Generate a report"

# Output in JSON format
claudethinkjson "What's the weather?"

# Set system message for context
claudethink --system "You are a helpful coding assistant" "Help me with Python"

# Control thinking budget
claudethink -b 64000 "Summarize this text"

# Read prompt from stdin
echo "What is the meaning of life?" | claudethink

# Interactive mode (press Ctrl+D to submit)
claudethink

# Check version
claudethink -v
```

CLI Options:
- `-s, --stream`: Stream the response in real-time
- `-t, --temperature`: Set response temperature (0.0 to 1.0, default: 1.0)
- `-m, --model`: Choose Claude model (default: claude-3-7-sonnet-20250219)
- `-b, --budget`: Set thinking budget in tokens (1 to 128000, default: 120000)
- `-f, --format`: Output format (text or JSON, default: text)
- `-o, --output`: Save response to specified file
- `--system`: Set system message for context
- `-d, --dry-run`: Test mode without making API calls
- `-v, --version`: Show version information

Available Models:
- claude-3-7-sonnet-20250219 (default)
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-3-haiku-20240307

## Development with Magic

The Magic toolchain enables a unified development experience for both Python and Mojo code. The project includes predefined tasks you can run with Magic:

```bash
# Install dependencies
magic install

# Run tests
magic run pixi task test

# Run Mojo-specific tests
magic run pixi task mojo-test

# Run linting
magic run pixi task lint

# Run type checking
magic run pixi task typecheck

# Format code
magic run pixi task format

# Build documentation
magic run pixi task docs-build

# Serve documentation locally
magic run pixi task docs

# Build the Python package
magic run pixi task build

# Build the Mojo binary
magic run pixi task mojo-build
```

## Testing

The project includes a comprehensive test suite covering all major functionality:

```bash
# Run all tests
magic run pixi task test

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
   magic run pixi task test
   magic run pixi task lint
   magic run pixi task typecheck
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