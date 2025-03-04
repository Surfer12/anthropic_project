# CLAUDE.md - Python Anthropic API Project

## Build/Test/Lint Commands
```bash
# Install dependencies
magic install

# Run the application
magic run python anthropic_client.py
# or 
magic run

# Lint with flake8
magic run flake8 *.py

# Type check with mypy
magic run mypy *.py

# Run tests (when added)
magic run pytest
```

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Maximum line length: 88 characters (Black default)
- Use type hints for function parameters and return values
- Class names: PascalCase (e.g., `AnthropicClient`)
- Function/variable names: snake_case (e.g., `get_response()`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_TOKENS`)
- Import order: standard library, third-party, local application
- Use f-strings for string formatting
- Environment variables should be loaded from .env using python-dotenv
- Always handle API exceptions and provide meaningful error messages
- Document functions with docstrings using Google style