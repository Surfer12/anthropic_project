# CLAUDE.md - Anthropic Project Development Guide

## Build/Test/Lint Commands
```bash
# Install dependencies
npm install                                  # JavaScript dependencies
pip install -e .                             # Python core
magic install                                # Mojo/ML dependencies

# Gradle (Java/Spring)
./gradlew build                              # Build all projects
./gradlew test --tests=TestName              # Run specific test
./gradlew qualityCheckAll                    # Run all quality checks

# Python
pytest tests/test_file.py::test_function     # Run specific test
pytest --cov=anthropic_client tests/         # Test with coverage
mypy src/python/anthropic_client             # Type-check code
flake8 anthropic_client                      # Lint code
pre-commit run --all-files                   # Run all pre-commit hooks

# Mojo
cd anthropic_client_mojo && magic run mojo main.mojo
magic run python -m anthropic_client.cli -m claude-3-5-haiku  # Run with specific model

# Node.js / Claude Code
npx claude-code                              # Run Claude Code CLI
```

## Code Style Guidelines

### Core Principles
- Consistent formatting with language-specific standards
- Meaningful variable names and descriptive comments
- Strong type hints/annotations in all languages
- Comprehensive error handling with context
- Thorough testing with clear test names
- Security best practices (no committed secrets)

### Python
- Follow PEP 8 and Black formatting (88 char line width)
- Snake_case for functions/variables, PascalCase for classes
- Use type hints and Google-style docstrings
- Import order: standard library, third-party, local
- Environment variables should use python-dotenv
- Handle exceptions with meaningful error messages

### Java
- Class names: PascalCase, methods/variables: camelCase
- Constants: UPPER_SNAKE_CASE
- Include JavaDoc for public classes/methods
- Prefer constructor injection for Spring dependencies

### JavaScript/Node.js
- Function names: camelCase, constants: UPPER_SNAKE_CASE
- Use ES6+ features, prefer const over let, avoid var
- Handle async with async/await and proper error handling

### Mojo
- Use Mojo 1.0+ syntax, snake_case for functions/variables
- Match Python implementations for feature parity
- Handle Python interop with appropriate ownership transfer
- Document workarounds for current Mojo limitations

### Testing
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies appropriately
- Test both success and failure cases
- Include edge cases and boundary conditions