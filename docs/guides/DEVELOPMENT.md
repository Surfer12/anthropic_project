# Development Rules and Guidelines

This document outlines the development practices and rules for the Anthropic API Client project.

## Environment Setup

### Using Magic (from Modular)

For all development tasks, use the Magic toolchain from Modular. The project is configured to work with Magic for dependency management and running Python scripts.

```bash
# Install dependencies
magic install

# Install the package in development mode
magic run pip install -e .
```

**IMPORTANT:** Always use `magic run` prefix when running Python commands during development:
```bash
# Correct
magic run pytest
magic run flake8
magic run python -m anthropic_client.cli

# Incorrect
pytest
flake8
python -m anthropic_client.cli
```

## Code Style and Standards

### Python

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Include docstrings for all modules, classes, and functions
- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)

### Testing

- Write tests for all new functionality
- Maintain test coverage above 90%
- Test both success and error cases
- Use mocks for external API calls

```bash
# Run all tests
magic run pytest

# Run tests with coverage
magic run pytest --cov=anthropic_client tests/

# Run specific test file
magic run pytest tests/test_specific_file.py
```

## Git Workflow

- Create feature branches from `main`
- Use descriptive commit messages
- Reference issue numbers in commit messages
- Keep commits focused on a single change
- Run tests before committing

```bash
# Create a feature branch
git checkout -b feature/descriptive-name

# Before committing
magic run pytest
magic run flake8

# Commit with reference to issue
git commit -m "Add feature X (resolves #123)"
```

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a release commit
4. Tag the release with version number
5. Push tags and commits to remote

## Documentation

- Update README.md for user-facing changes
- Update CLI.md for command-line interface changes
- Document all environment variables in appropriate files
- Ensure examples are up-to-date

## Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors with appropriate levels
- Handle all external API errors

## Dependency Management

- All dependencies should be specified in `pyproject.toml`
- Pin dependency versions where appropriate
- Document any new dependencies in README.md
- Review dependencies regularly for updates and security issues

## API Usage

- Use environment variables for credentials
- Implement rate limiting and retry logic
- Log API requests and responses (without sensitive data)
- Handle API errors gracefully

## Performance Considerations

- Minimize API calls
- Use streaming responses for large outputs
- Implement pagination for large datasets
- Profile and optimize performance-critical code

## Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Validate and sanitize all user inputs
- Follow security best practices for HTTP requests