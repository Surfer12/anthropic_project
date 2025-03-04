# Anthropic API Client

This project demonstrates how to use the Anthropic Python library to interact with Claude models.

## Setup

1. This project uses Magic (from Modular) for package management.
   ```bash
   magic install
   ```

2. Create a `.env` file with your Anthropic API key:
   ```bash
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

3. Run the script:
   ```bash
   magic run python anthropic_client.py
   ```

## Features

- Uses Claude 3.7 Sonnet model
- Enables the "thinking" capability
- Supports 128k context and 64k thinking budget
- Uses streaming to display responses in real-time
- Loads API key from `.env` file using python-dotenv

## Testing

The project includes a comprehensive test suite:

```bash
# Run all tests
magic run pytest

# Run tests with verbose output
magic run pytest -v

# Run a specific test file
magic run pytest tests/test_anthropic_client.py
```

## Dependencies

- anthropic - Core API client library
- python-dotenv - Environment variable management
- pytest - Testing framework
- flake8 - Code linting
- mypy - Type checking