# Anthropic API Client

This project demonstrates how to use the Anthropic Python library to interact with Claude models.

## Setup

1. This project uses Magic (from Modular) for package management.

2. You'll need to set your Anthropic API key as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

3. Run the script:
   ```bash
   python anthropic_client.py
   ```

## Features

- Uses Claude 3.7 Sonnet model
- Enables the "thinking" capability
- Supports 128k output tokens