# CLAUDE.md - Python & Mojo Anthropic API Project

## Build/Test/Lint Commands

```bash
# Install dependencies
magic install

# Run the Python application
magic run python anthropic_client.py
# or 
magic run

# Run the Mojo application
cd anthropic_client_mojo
magic run mojo main.mojo

# Lint Python with flake8
magic run flake8 *.py

# Type check Python with mypy
magic run mypy *.py

# Run tests with coverage
magic run pytest --cov=anthropic_client tests/

# Generate coverage report
magic run pytest --cov=anthropic_client --cov-report=html tests/

# Run specific test categories
magic run pytest tests/test_anthropic_client.py  # Core client tests
magic run pytest tests/test_cli.py               # CLI interface tests
magic run pytest tests/test_integration.py       # Integration tests
magic run pytest tests/test_environment.py       # Environment tests
```

## Testing Guidelines

### Test Categories
1. **Unit Tests**
   - Core client functionality
   - Parameter validation
   - Error handling
   - Response parsing

2. **Integration Tests**
   - API communication
   - Streaming responses
   - Rate limiting
   - Authentication

3. **Environment Tests**
   - Configuration loading
   - API key handling
   - Environment variables

4. **CLI Tests**
   - Command parsing
   - Input/output handling
   - Interactive mode
   - Error display

### Test Best Practices
- Use descriptive test names that explain the scenario
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test both success and failure cases
- Include edge cases and boundary conditions
- Keep tests focused and atomic
- Use appropriate assertions
- Clean up resources in teardown

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

### Mojo
- Use Mojo 1.0+ syntax (no `let` keyword, use `var` instead)
- Class names: PascalCase (e.g., `AnthropicClient`)
- Function/variable names: snake_case (e.g., `get_response()`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_TOKENS`)
- Import order: standard library, third-party, local application
- Use proper Python interoperability for API communication
- Maintain consistent error handling with Python implementation
- Document functions with docstrings
- For Python interop, import `PythonObject` from the `python` module
- Match Mojo implementation closely with Python counterpart for feature parity

### Known Mojo Issues and Workarounds

#### Python Object Attribute Access
- Use `PythonObject.`.`__getattr__()` method instead of dot notation when accessing attributes that cause linting errors
- Example: `obj.__getattr__("attribute_name")` instead of `obj.attribute_name`
- Add comments to indicate why this pattern is being used

#### Memory Management Functions
- Use explicit ownership transfer with `^` or `.steal()` when appropriate
- Implement proper cleanup in destructors or with `try`/`finally` blocks
- Consider using `owned` pointer types for objects that need explicit lifetime management
- Add todo comments for future refactoring once Mojo's memory management features improve

#### Module Imports
- Use fully qualified import paths to avoid ambiguity
- When importing from Python, prefer `from python import Python, PythonObject` pattern
- For modules that can't be properly imported, create wrapper functions that use Python interop
- Document import workarounds with comments to revisit in future Mojo versions

### Error Handling
- Use specific exception types
- Include context in error messages
- Log errors appropriately
- Clean up resources in finally blocks
- Handle API-specific errors
- Implement proper retry logic
- Validate input parameters
- Handle timeouts gracefully

### Logging
- Use appropriate log levels:
  - DEBUG: Detailed information for debugging
  - INFO: General operational events
  - WARNING: Unexpected but handled situations
  - ERROR: Serious problems that need attention
- Include relevant context in log messages
- Don't log sensitive information
- Use structured logging where appropriate
- Configure logging based on environment

### Security
- Never commit API keys or secrets
- Use environment variables for configuration
- Validate and sanitize all inputs
- Handle sensitive data appropriately
- Follow secure coding practices
- Implement proper rate limiting
- Use HTTPS for all API calls
- Regular dependency updates

### Documentation
- Keep README.md up to date
- Document all public interfaces
- Include usage examples
- Explain error scenarios
- Document configuration options
- Maintain changelog
- Include troubleshooting guide