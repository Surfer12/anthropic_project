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

### Command-Line Tools (Recommended)

We provide several command-line tools for easy interaction with Claude:

```bash
# Install the CLI tools
chmod +x claudethink_install
./claudethink_install
```

Then follow the instructions to add the tools to your PATH.

```bash
# Basic usage - send a prompt to Claude
claudethinkmojo "What is the capital of France?"

# Stream the response in real-time
claudethinkstream "Tell me a story"

# Use lower temperature for more deterministic responses
claudethinkfast "Solve this math problem"

# Test mode without making API calls
claudethinkdry "This is a test prompt"

# Get response in JSON format
claudethinkjson "List the top 5 programming languages" > languages.json

# Use the faster Haiku model
claudethinkhaiku "Give me a quick summary of the French Revolution"

# Save response to a file
claudethinkfile output.md "Write documentation for a REST API"
```

See [CLI.md](CLI.md) for complete documentation on the command-line tools.

### Python CLI (Direct Usage)

You can also use the Python CLI directly:

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

### CLI Options

The Python CLI supports these options:

- `prompt`: The prompt to send to Claude. If not provided, reads from stdin.
- `-s, --stream`: Stream the response as it's generated
- `-t, --temperature`: Temperature for response generation (0.0 to 1.0)
- `-m, --model`: Claude model to use
- `-b, --budget`: Thinking budget in tokens (1 to 128000)
- `-f, --format`: Output format (text or JSON)
- `-o, --output`: Save response to specified file
- `--system`: System message to set context for Claude
- `-d, --dry-run`: Test mode that doesn't make actual API calls
- `-v, --version`: Show program's version number and exit

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