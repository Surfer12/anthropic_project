# CLI Utility Scripts

This directory contains convenient shortcut scripts for using the Claude API with different configurations.

## Available Scripts

- **claudethinkhaiku** - Uses the Claude Haiku model for faster responses (claude-3-5-haiku-20241022)
- **claudethinksonnet** - Uses the Claude Sonnet model for balanced performance (claude-3-5-sonnet-20240620)
- **claudethinknostream** - Disables streaming for batch processing (using the -ns flag)

## Usage

These scripts need to be in your PATH to be executed from anywhere. You can run:

```bash
chmod +x /Users/ryanoates/anthropic_project/anthropic_client/bin/*
```

Then add this directory to your PATH in your shell profile (e.g., .bashrc or .zshrc):

```bash
export PATH="$PATH:/Users/ryanoates/anthropic_project/anthropic_client/bin"
```

## Examples

```bash
# Use Haiku for a quick response
claudethinkhaiku "What is the meaning of life?"

# Use Sonnet for a more detailed response
claudethinksonnet "Explain quantum computing"

# Disable streaming for scripting
claudethinknostream "Give me the capital of France" > france_info.txt
```

## Creating Custom Scripts

You can create your own custom scripts following the same pattern:

```bash
#!/bin/bash
cd /Users/ryanoates/anthropic_project/
python -m anthropic_client.cli [OPTIONS] "$@"
```

Common options include:
- `-m MODEL_NAME`: Specify the model to use
- `-ns`: Disable streaming (streaming is on by default)
- `-t TEMPERATURE`: Set the temperature for responses