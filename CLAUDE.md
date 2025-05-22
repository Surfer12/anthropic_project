# CLAUDE.md - Anthropic Project Development Guide

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Anthropic Project is a multi-language client and CLI for interacting with Claude AI and orchestrating multiple model providers, offering seamless switching between Anthropic and OpenAI models with a unified API.

**Key Innovation:** Multi-provider model integration with a single unified client interface.

**Project Status:** Development

## Repository Structure

- **anthropic_client/**: Python client implementation for Anthropic models
- **anthropic_client_mojo/**: Mojo client code for model operations
- **scripts/**: Utility scripts and Docker configurations
- **src/**: Source code for various language bindings
- **config/**: JSON and YAML configuration files for model parameters
- **tests/**: Test suites for Python, Java, and Mojo components
- **docs/**: Project documentation and examples
- **bin/**: CLI entry points and supplementary binaries

## Build and Development Commands

### Python Components

```bash
# Install dependencies
pip install -r requirements.txt
python -m pip install -e .

# Run tests
pytest tests/
pytest tests/test_file.py::test_function

# Type checking and linting
mypy src/python/anthropic_client
flake8 anthropic_client
```

### Java Components

```bash
# Gradle build
./gradlew build
./gradlew test --tests=TestName

# Quality checks
./gradlew qualityCheckAll
```

### JavaScript/TypeScript Components

```bash
# Install dependencies
npm install

# Run CLI
npx claude-code

# Linting and formatting
npm run lint
npm run format
```

### Mojo Components

```bash
# Install dependencies 
cd anthropic_client_mojo
magic install

# Run Mojo code
magic run mojo main.mojo
magic run python -m anthropic_client.cli -m claude-3-5-haiku
```

### Other Useful Commands

```bash
# Pre-commit checks
pre-commit run --all-files
```

## Architectural Patterns

### Multi-Provider Integration

This project implements a flexible integration system allowing custom OpenAI models to be used alongside Anthropic's Claude models.

**Key Components:**
- **Model Configuration Loader**: Loads JSON model configs from multiple locations
- **MultiProviderClient**: Routes requests to the appropriate API based on model type
- **ModelName Enum**: Defines providers and parameters for supported models

### Error Handling & Resilience (Optional)

Detailed best practices for error context propagation and retry mechanisms

## Code Style Guidelines

### Universal Principles
- **Type Safety**: Strong typing and validation across all languages
- **Meaningful Names**: Descriptive identifiers
- **Error Handling**: Context-rich exceptions
- **Documentation**: Clear docstrings/comments
- **Security**: No secrets committed

### Python
- Follow PEP 8, use snake_case, type hints, Google-style docstrings

### Java
- JDK 17+, PascalCase for classes, camelCase for methods, Javadoc for public APIs

### JavaScript/TypeScript
- ES6+, camelCase, async/await, strong TypeScript typing

### Mojo
- Mojo 1.0+ syntax, snake_case, interop considerations

## Testing Guidelines

- AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Cover both success and failure cases
- Edge case testing and boundary conditions
- Maintain test coverage above 80%

## Integration Points

Describe how this project integrates with Anthropic's API and any other services

## Performance Considerations

Key performance patterns, caching strategies, and optimizations

## Deployment

Instructions for deploying CLI and services to production environments

## Important Notes

- Environment variables should be managed via python-dotenv
- Configuration files in `config/` directory override defaults
- Refer to the Unified Development Ethos for ecosystem-wide guidelines