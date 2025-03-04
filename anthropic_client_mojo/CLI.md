# CLI.md - Command-Line Shortcuts for Claude Mojo

This file contains useful command-line shortcuts and script definitions for working with the Anthropic Claude API using our Mojo implementation.

## Command-Line Shortcuts

### 1. claudethinkmojo

This is the main script that sends a prompt to Claude through our Mojo client implementation with thinking enabled.

```bash
#!/bin/bash
# claudethinkmojo - Send a prompt to Claude with thinking enabled (Mojo version)

cd /Users/ryanoates/anthropic_project/anthropic_client_mojo
magic run mojo main.mojo "$@"
```

### 2. claudethinkstream

This script sends a prompt to Claude and streams the response with thinking enabled.

```bash
#!/bin/bash
# claudethinkstream - Stream a response from Claude with thinking enabled (Mojo version)

cd /Users/ryanoates/anthropic_project/anthropic_client_mojo
magic run mojo main.mojo -s "$@"
```

### 3. claudethinkfast

This script sends a prompt to Claude with a lower temperature (0.3) for more deterministic responses.

```bash
#!/bin/bash
# claudethinkfast - Send a prompt to Claude with lower temperature (Mojo version)

cd /Users/ryanoates/anthropic_project/anthropic_client_mojo
magic run mojo main.mojo -t 0.3 "$@"
```

### 4. claudethinkdry

This script runs in dry-run mode, useful for testing without making actual API calls.

```bash
#!/bin/bash
# claudethinkdry - Test Claude interaction without making API calls (Mojo version)

cd /Users/ryanoates/anthropic_project/anthropic_client_mojo
magic run python python_cli.py -d "$@"
```

## Installation

To install these scripts:

1. Copy the script content to a new file in your PATH (e.g., `/usr/local/bin/claudethinkmojo`)
2. Make them executable:

```bash
chmod +x /usr/local/bin/claudethinkmojo
chmod +x /usr/local/bin/claudethinkstream
chmod +x /usr/local/bin/claudethinkfast
chmod +x /usr/local/bin/claudethinkdry
```

## Usage Examples

```bash
# Send a direct prompt
claudethinkmojo "Explain quantum computing in simple terms"

# Use with piped input
cat document.txt | claudethinkmojo

# Stream the response
claudethinkstream "Write a short poem about coding"

# Get more deterministic responses
claudethinkfast "What are the five largest planets in our solar system?"

# Test without making API calls
claudethinkdry "This is a test prompt"
```

## Configuration

These scripts use the ANTHROPIC_API_KEY environment variable. Ensure it's set in your environment or in a .env file in the project directory.

```bash
# Add to your .bashrc, .zshrc, or equivalent
export ANTHROPIC_API_KEY="your-api-key-here"
```

Alternatively, create a .env file in the project directory:

```
ANTHROPIC_API_KEY=your-api-key-here
```