# CLAUDE.md - Development Guide

## Build/Test/Lint Commands
```bash
# Install dependencies
npm install
pip install -e .

# Java/Spring Boot application
./gradlew bootRun                   # Run the Spring Boot application
./gradlew build                     # Build the entire project
./gradlew test                      # Run all tests
./gradlew test --tests=TestName     # Run a specific test
./gradlew codeQualityCheck          # Run checkstyle, PMD, and spotbugs
./gradlew jacocoTestReport          # Generate test coverage report

# Python commands
pytest                              # Run all Python tests
pytest tests/test_file.py::test_fn  # Run a specific test
flake8 anthropic_client             # Lint Python code
mypy anthropic_client               # Type-check Python code

# Mojo commands (in mojo directories)
cd src/mojo && magic run mojo file.mojo  # Run Mojo file
```

## Code Style Guidelines

### Java
- Class names: PascalCase (e.g., `ModelArchitecture`)
- Methods/variables: camelCase (e.g., `computeScore()`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_SIZE`)
- Follow Spring Boot conventions for controllers and services
- Always include JavaDoc for public classes and methods
- Use explicit error handling with custom exceptions
- Prefer constructor injection for dependencies

### JavaScript/Node.js
- Function names: camelCase (e.g., `calculateTotal()`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_SIZE`)
- Use ES6+ features (arrow functions, destructuring)
- Prefer `const` over `let`, avoid `var`
- Handle async operations with async/await
- Use proper error handling with try/catch blocks

### Python/Mojo
- Function names: snake_case (e.g., `calculate_total()`)
- Class names: PascalCase (e.g., `ModelTrainer`)
- Use type hints where appropriate
- Follow PEP 8 guidelines (88 char line limit)
- For Mojo: use fully qualified import paths
- Document functions with Google-style docstrings
- Handle API exceptions with meaningful error messages