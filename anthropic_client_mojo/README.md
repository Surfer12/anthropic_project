# Anthropic API Client - Mojo Version

This is a Mojo 🔥 version of the Anthropic Claude API client, providing the same functionality as the Python version but with the performance and systems programming capabilities of Mojo.

## Features

- **Advanced Model Support**: Uses Claude 3.7 Sonnet model with 128k context window
- **Enhanced Capabilities**:
  - Thinking capability enabled with 120k token budget
  - Temperature control for response randomness (0.0 to 1.0)
  - Streaming support for real-time responses
  - Comprehensive error handling
- **Mojo Advantages**:
  - Type safety and strong type system
  - Memory safety without garbage collection
  - High performance compiled code
  - Python interoperability

## Project Structure

```
anthropic_client_mojo/
├── client.mojo    # Core client implementation
├── cli.mojo       # Command-line interface
├── main.mojo      # Entry point
└── README.md      # Documentation
```

## Prerequisites

- [Mojo SDK](https://www.modular.com/mojo) installed
- Python 3.8+ with the Anthropic Python SDK and python-dotenv installed:
  ```bash
  pip install anthropic python-dotenv
  ```

## Installation

1. Clone this repository
2. Build the Mojo executable:
   ```bash
   cd anthropic_client_mojo
   mojo build -o claudemojo main.mojo
   ```
3. Make the executable available in your PATH

## Environment Setup

Create a `.env` file with your Anthropic API key:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## Usage

```bash
# Direct prompt
./claudemojo "What is the capital of France?"

# Stream the response
./claudemojo -s "Tell me a story"

# Control temperature
./claudemojo -t 0.2 "Solve this math problem"

# Read prompt from stdin
echo "What is the meaning of life?" | ./claudemojo

# Interactive mode (press Ctrl+D to submit)
./claudemojo
```

CLI Options:
- `-s, --stream`: Stream the response in real-time
- `-t, --temperature`: Set response temperature (0.0 to 1.0, default: 1.0)

## Notes on Mojo Implementation

This Mojo implementation:

1. Uses Mojo's Python interoperability to maintain compatibility with the Anthropic SDK
2. Leverages Mojo's struct system for organizing code
3. Provides proper error handling with Mojo's error system
4. Maintains the same CLI interface as the Python version

Mojo is still evolving, and this implementation may be updated as new Mojo features become available.

## Performance

While the current implementation primarily uses Python interoperability, future versions could leverage Mojo's performance capabilities for tasks such as:

- Parallel processing of large responses
- Efficient streaming implementations
- Memory-efficient handling of token processing
- Integration with native Mojo data structures

## License

This project is licensed under the MIT License - see the LICENSE file for details.