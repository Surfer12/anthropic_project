# CLI.md - Command-Line Shortcuts for Claude Mojo

This file contains useful command-line shortcuts and script definitions for working with the Anthropic Claude API using our Mojo/Python implementation.

## Command-Line Shortcuts

### 1. claudethinkmojo

This is the main script that sends a prompt to Claude with thinking enabled.

```bash
#!/bin/bash
# claudethinkmojo - Send a prompt to Claude with thinking enabled

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"
magic run python "$PROJECT_DIR/python_cli.py" "$@"
```

### 2. claudethinkstream

This script sends a prompt to Claude and streams the response with thinking enabled.

```bash
#!/bin/bash
# claudethinkstream - Stream a response from Claude with thinking enabled

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"
magic run python "$PROJECT_DIR/python_cli.py" -s "$@"
```

### 3. claudethinkfast

This script sends a prompt to Claude with a lower temperature (0.3) for more deterministic responses.

```bash
#!/bin/bash
# claudethinkfast - Send a prompt to Claude with lower temperature

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"
magic run python "$PROJECT_DIR/python_cli.py" -t 0.3 "$@"
```

### 4. claudethinkdry

This script runs in dry-run mode, useful for testing without making actual API calls.

```bash
#!/bin/bash
# claudethinkdry - Test Claude interaction without making API calls

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"
magic run python "$PROJECT_DIR/python_cli.py" -d "$@"
```

### 5. claudethinkjson

This script returns Claude's response in JSON format.

```bash
#!/bin/bash
# claudethinkjson - Get Claude's response in JSON format

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"
magic run python "$PROJECT_DIR/python_cli.py" -f json "$@"
```

### 6. claudethinkhaiku

This script uses the smaller, faster Claude Haiku model.

```bash
#!/bin/bash
# claudethinkhaiku - Use the Claude Haiku model (smaller/faster)

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"
magic run python "$PROJECT_DIR/python_cli.py" -m claude-3-5-haiku-20241022 "$@"
```

### 7. claudethinkfile

This script saves Claude's response to a specified file.

```bash
#!/bin/bash
# claudethinkfile - Save Claude's response to a file

PROJECT_DIR="/Users/ryanoates/anthropic_project/anthropic_client_mojo"
cd "$PROJECT_DIR"
export PIXI_PROJECT_MANIFEST="$PROJECT_DIR/pixi.toml"

if [ "$#" -lt 2 ]; then
  echo "Usage: claudethinkfile <output_file> <prompt>"
  exit 1
fi

output_file="$1"
shift
magic run python "$PROJECT_DIR/python_cli.py" -o "$output_file" "$@"
```

## Installation

There are three ways to install these scripts:

### 1. Using the Installation Script

Run the provided installation script:

```bash
chmod +x /Users/ryanoates/anthropic_project/anthropic_client_mojo/claudethink_install
./claudethink_install
```

Then choose one of the installation methods it suggests.

### 2. Copy to /usr/local/bin

```bash
sudo cp /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/* /usr/local/bin/
```

### 3. Create Symlinks (Recommended)

```bash
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkmojo /usr/local/bin/claudethinkmojo
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkstream /usr/local/bin/claudethinkstream
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkfast /usr/local/bin/claudethinkfast
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkdry /usr/local/bin/claudethinkdry
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkjson /usr/local/bin/claudethinkjson
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkhaiku /usr/local/bin/claudethinkhaiku
sudo ln -s /Users/ryanoates/anthropic_project/anthropic_client_mojo/bin/claudethinkfile /usr/local/bin/claudethinkfile
```

### 4. Add to PATH (Alternative)

Add the bin directory to your PATH in your shell profile:

```bash
echo 'export PATH="/Users/ryanoates/anthropic_project/anthropic_client_mojo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
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

# Get response in JSON format
claudethinkjson "List the top 5 programming languages" > languages.json

# Use the faster Haiku model
claudethinkhaiku "Give me a quick summary of the French Revolution"

# Save response to a file
claudethinkfile output.md "Write documentation for a REST API"
```

## Available Options in python_cli.py

All scripts are based on python_cli.py, which supports these options:

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