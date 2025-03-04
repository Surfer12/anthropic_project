# Anthropic Claude API Client - Mojo/Python Hybrid

This is a hybrid Mojo/Python implementation of the Anthropic Claude API client, leveraging both the performance and systems programming capabilities of Mojo and the mature ecosystem of Python.

## Features

- **Advanced Model Support**: Uses Claude 3.7 Sonnet model with 128k context window
- **Enhanced Capabilities**:
  - Thinking capability enabled with 120k token budget
  - Temperature control for response randomness (0.0 to 1.0)
  - Streaming support for real-time responses
  - Comprehensive error handling
  - Dry-run mode for testing without API calls
- **Hybrid Approach**:
  - Mojo for structure, typing, and performance-critical code
  - Python for API interaction and complex operations
  - Seamless interoperability between both languages

## Project Structure

```
anthropic_client_mojo/
├── client.mojo     # Core client implementation
├── cli.mojo        # Command-line interface (Mojo)
├── main.mojo       # Mojo application entry point
├── python_cli.py   # Python implementation of CLI
├── tests.mojo      # Test suite
└── README.md       # Documentation
```

## Prerequisites

- Magic installed (Python package manager and Mojo runtime)
- Python 3.8+ 

## Installation

1. Clone this repository
2. Set up your environment with Magic:
   ```bash
   cd anthropic_client_mojo
   magic init
   magic add python-dotenv
   magic add anthropic
   ```

## Environment Setup

Create a `.env` file with your Anthropic API key:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## Usage

### Python CLI (Recommended)

```bash
# Direct prompt
magic run python python_cli.py "What is the capital of France?"

# Stream the response
magic run python python_cli.py -s "Tell me a story"

# Control temperature
magic run python python_cli.py -t 0.2 "Solve this math problem"

# Test mode (no API calls)
magic run python python_cli.py -d "This is a test prompt"

# Read prompt from stdin (press Ctrl+D to submit)
magic run python python_cli.py
```

### Mojo Interface

The Mojo interface is still experimental and currently suggests using the Python CLI:

```bash
magic run mojo main.mojo
```

### Running Tests

Tests can be run in dry-run mode without making actual API calls:

```bash
magic run mojo tests.mojo --dry-run
```

CLI Options:
- `-s, --stream`: Stream the response in real-time
- `-t, --temperature`: Set response temperature (0.0 to 1.0, default: 1.0)
- `-d, --dry-run`: Test mode without making API calls

## Implementation Notes

This implementation:

1. Uses a hybrid approach with Python handling the API interactions
2. Leverages Mojo's struct system and type safety where beneficial
3. Provides proper error handling for both languages
4. Maintains a consistent interface across Python and Mojo versions

Mojo is still evolving, and this implementation will be updated as new Mojo features become available.

## Future Enhancements

As Mojo matures, this project aims to:

1. Gradually move more functionality from Python to native Mojo
2. Enhance error handling for API interactions
3. Develop a more comprehensive test suite
4. Leverage Mojo's performance capabilities for:
   - Parallel processing of large responses
   - Memory-efficient token processing
   - Enhanced streaming implementations

## License

This project is licensed under the MIT License - see the LICENSE file for details.