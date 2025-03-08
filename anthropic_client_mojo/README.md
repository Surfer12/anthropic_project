# Anthropic API Client - Mojo Implementation

This directory contains the Mojo implementation of the Anthropic API client. The Mojo version provides better performance compared to the standard Python implementation.

## Files Overview

- `client.mojo`: Core client implementation for interacting with Anthropic's Claude models
- `cli.mojo`: Command-line interface implementation
- `tests.mojo`: Tests for the Mojo implementation
- `python_cli.py`: Python bridge to the Mojo implementation for CLI usage
- `claudethink_install`: Installation script for the CLI tools

## Why Mojo?

Mojo combines Python's usability with C++'s performance. For this project, using Mojo offers several advantages:

1. **Better Performance**: Faster response processing and handling
2. **Type Safety**: Strong typing helps catch errors at compile time
3. **Memory Efficiency**: Better memory management for handling large responses
4. **Python Interoperability**: Seamless integration with Python code

## Using the Mojo Implementation

### Prerequisites

Make sure you have the Magic toolchain installed:
```bash
curl https://get.modular.com | sh
```

### Installation

1. Install the package:
```bash
cd ..  # Go to the project root
magic install
```

2. Install the CLI tools:
```bash
magic run pixi task install-cli
```

### CLI Usage

Once installed, you can use the Mojo-powered CLI:
```bash
claudethinkmojo "What is the capital of France?"
```

### Direct Mojo Usage

You can also run Mojo files directly:
```bash
cd antropic_client_mojo
magic run mojo run client.mojo
```

### Testing

Run the Mojo tests:
```bash
magic run mojo run tests.mojo
```

## Building from Source

To build a standalone binary:
```bash
magic run mojo build cli.mojo -o claudethinkmojo_binary
```

## Development Notes

- This implementation uses Python interoperability to access certain libraries
- The core logic is implemented in Mojo for better performance
- The CLI is exposed via both native Mojo and Python bridge interfaces
- Tests ensure compatibility with the Python implementation

## Python Bridge

The `python_cli.py` file serves as a bridge between Python and the Mojo implementation, allowing users to leverage the Mojo implementation's performance while maintaining a Python-like interface.

## Contributing

When contributing to the Mojo implementation:

1. Make sure to run tests: `magic run mojo run tests.mojo`
2. Keep Python compatibility in mind
3. Document new features and performance improvements
4. Update both implementations when adding new features