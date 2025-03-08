# Magic Integration Guide

This project fully embraces Modular's Magic toolchain for dependency management, testing, and building both Python and Mojo components. This guide explains how to get the most out of Magic integration.

## What is Magic?

Magic is Modular's developer toolchain that makes working with AI and high-performance computing easier by unifying the Python and Mojo ecosystems. It provides a streamlined way to:

- Manage dependencies for Python and Mojo in a unified way
- Build, test, and run applications with consistent environments
- Deploy applications with reproducible environments

## Installation

1. **Install Magic** (if not already installed):
   ```bash
   curl https://get.modular.com | sh
   ```

2. **Verify installation**:
   ```bash
   magic --version
   ```

## Using Magic with this Project

### Basic Commands

- **Install dependencies**:
  ```bash
  magic install
  ```

- **Run a Python script**:
  ```bash
  magic run python script.py
  ```

- **Run a Mojo script**:
  ```bash
  magic run mojo run script.mojo
  ```

- **Build a Mojo binary**:
  ```bash
  magic run mojo build script.mojo -o output
  ```

### Pixi Integration

This project uses Pixi (via the `pixi.toml` file) to define dependencies and tasks. You can run these tasks with:

```bash
magic run pixi task <task_name>
```

Available tasks include:

- `test`: Run the test suite
- `lint`: Run code linting
- `typecheck`: Run type checking
- `format`: Format code
- `docs`: Serve documentation locally
- `docs-build`: Build documentation
- `build`: Build the Python package
- `mojo-build`: Build the Mojo binary
- `install-cli`: Install the CLI tools

### Environment Variables

Magic respects environment variables defined in the `.env` file at the project root. Important environment variables include:

- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `MODEL`: The Claude model to use (defaults to claude-3-7-sonnet-20250219)
- `MAX_TOKENS`: Maximum tokens for responses
- `THINKING_BUDGET`: Token budget for thinking capability
- `TEMPERATURE`: Temperature for response randomness
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Working with Mojo

### Python-Mojo Interoperability

This project demonstrates how to use Mojo alongside Python:

1. **Core functionality in Mojo**: High-performance parts of the client are written in Mojo
2. **Python bridge**: Python can call Mojo functions through the Python interoperability layer
3. **CLI integration**: The command-line tools can use either the Python or Mojo implementations

### Mojo Development Tips

- Mojo code is in the `anthropic_client_mojo` directory
- The `client.mojo` file contains the core client implementation
- The `cli.mojo` file contains the command-line interface
- The `tests.mojo` file contains Mojo-specific tests
- The `python_cli.py` file provides a Python bridge to the Mojo implementation

## Continuous Integration

In CI environments, you can use Magic with the following steps:

```yaml
# Example GitHub Actions workflow
name: CI with Magic

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Magic
        run: curl https://get.modular.com | sh
      - name: Install dependencies
        run: magic install
      - name: Run tests
        run: magic run pixi task test
      - name: Run linting
        run: magic run pixi task lint
      - name: Run type checking
        run: magic run pixi task typecheck
```

## Troubleshooting

### Common Issues

1. **Environment variables not being recognized**:
   - Make sure your `.env` file is at the project root
   - Run commands from the project root, or set the `PIXI_PROJECT_MANIFEST` environment variable

2. **Magic not finding Mojo**:
   - Ensure Magic is properly installed
   - Run `magic install` to update dependencies

3. **Dependency conflicts**:
   - Check `pixi.toml` for version constraints
   - Try removing `.magic/envs` and running `magic install` again

### Getting Help

- [Magic Documentation](https://docs.modular.com/magic)
- [Mojo Documentation](https://docs.modular.com/mojo)
- [Project Issues](https://github.com/yourusername/anthropic_client/issues)
