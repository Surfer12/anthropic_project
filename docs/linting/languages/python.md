# Python Linting Configuration

## Overview

This document details the Python-specific linting configuration and tools used in our codebase. Our Python linting infrastructure is designed to ensure code quality, maintainability, and consistency across all Python modules.

## Tool Stack

### 1. Black (Code Formatter)
- Version: 24.1.1
- Purpose: Automated code formatting
- Configuration: `pyproject.toml`
- Key settings:
  ```toml
  [tool.black]
  line-length = 100
  target-version = ['py39']
  include = '\.pyi?$'
  extend-exclude = '''
  # Exclude patterns
  (
    \.eggs
    | \.git
    | \.mypy_cache
    | build
    | dist
  )
  '''
  ```

### 2. Flake8 (Style Guide Enforcement)
- Version: 7.0.0
- Purpose: Style guide enforcement and code analysis
- Configuration: `.flake8`
- Key rules:
  ```ini
  [flake8]
  max-line-length = 100
  extend-ignore = E203, W503
  max-complexity = 10
  per-file-ignores =
      __init__.py: F401
  exclude =
      .git,
      __pycache__,
      build,
      dist
  ```

### 3. mypy (Static Type Checker)
- Version: 1.8.0
- Purpose: Static type checking
- Configuration: `pyproject.toml`
- Key settings:
  ```toml
  [tool.mypy]
  python_version = "3.9"
  warn_return_any = true
  warn_unused_configs = true
  disallow_untyped_defs = true
  disallow_incomplete_defs = true
  check_untyped_defs = true
  disallow_untyped_decorators = true
  no_implicit_optional = true
  warn_redundant_casts = true
  warn_unused_ignores = true
  warn_no_return = true
  warn_unreachable = true
  ```

### 4. isort (Import Sorter)
- Version: 5.13.2
- Purpose: Import statement organization
- Configuration: `pyproject.toml`
- Key settings:
  ```toml
  [tool.isort]
  profile = "black"
  line_length = 100
  multi_line_output = 3
  include_trailing_comma = true
  force_grid_wrap = 0
  use_parentheses = true
  ensure_newline_before_comments = true
  ```

## Type System Guidelines

### Type Annotation Standards
1. All function parameters and return types must be annotated
2. Use type aliases for complex types
3. Prefer composition over inheritance for type definitions
4. Document type variables and constraints

### Common Type Patterns
```python
from typing import TypeVar, Protocol, Optional, Sequence

T = TypeVar('T', bound='BaseClass')
class DataProcessor(Protocol[T]):
    def process(self, data: Sequence[T]) -> Optional[T]: ...
```

### Type Ignore Directives
- Use sparingly and only with proper justification
- Document reason for type ignore
- Track with `type_system_refiner.py`
- Regular review and cleanup

## Code Style Guidelines

### Naming Conventions
1. Class names: `PascalCase`
2. Function/variable names: `snake_case`
3. Constants: `UPPER_SNAKE_CASE`
4. Private attributes: `_leading_underscore`

### Function Design
1. Maximum length: 50 lines
2. Single responsibility principle
3. Clear parameter names
4. Descriptive docstrings

### Documentation Standards
1. Google-style docstrings
2. Type hints in docstrings for Python < 3.6
3. Example usage in docstrings
4. Module-level docstrings

Example:
```python
def process_data(data: list[str], *, threshold: float = 0.5) -> dict[str, float]:
    """Process string data and return analysis results.

    Args:
        data: List of strings to process
        threshold: Minimum confidence threshold (default: 0.5)

    Returns:
        Dictionary mapping strings to their confidence scores

    Raises:
        ValueError: If threshold is not between 0 and 1
    """
```

## Error Handling

### Exception Guidelines
1. Use custom exceptions for domain-specific errors
2. Include context in error messages
3. Document expected exceptions
4. Clean up resources in finally blocks

### Logging Standards
1. Use structured logging
2. Include relevant context
3. Appropriate log levels
4. Consistent format

## Testing Requirements

### Test Structure
1. Use pytest
2. Organize tests by feature
3. Clear test names
4. Comprehensive assertions

### Coverage Requirements
1. Minimum 90% coverage
2. Critical paths: 100%
3. Exception handling coverage
4. Edge case coverage

## Common Issues and Solutions

### Import Management
1. Absolute imports preferred
2. Group imports by source
3. Remove unused imports
4. Use import aliases judiciously

### Performance Considerations
1. Use appropriate data structures
2. Profile critical code paths
3. Optimize hot spots
4. Document performance requirements

### Resource Management
1. Use context managers
2. Close resources explicitly
3. Handle cleanup in finally blocks
4. Monitor resource usage

## Tooling Integration

### Pre-commit Configuration
```yaml
repos:
-   repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
    -   id: flake8
-   repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
    -   id: isort
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]
```

### IDE Integration
1. VSCode settings
2. PyCharm configuration
3. Sublime Text setup
4. Vim/Neovim configuration

## Maintenance

### Regular Tasks
1. Update tool versions
2. Review configuration
3. Update documentation
4. Monitor compliance

### Version Control
1. Track configuration changes
2. Document updates
3. Migration guides
4. Changelog maintenance 