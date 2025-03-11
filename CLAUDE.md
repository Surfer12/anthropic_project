# CLAUDE.md - Development Guide

## Build/Test/Lint Commands
```bash
# Install dependencies
npm install
pip install -e .
magic install  # For Max/ML work

# Gradle commands (Java/Spring Boot)
./gradlew bootRun                   # Run the application
./gradlew build                     # Build all projects
./gradlew testAll                   # Run all tests
./gradlew test --tests=TestName     # Run a specific test
./gradlew qualityCheckAll           # Run all quality checks
./gradlew setupDev                  # Setup development environment

# Python commands
pytest                                     # Run all tests
pytest tests/test_file.py::test_function   # Run a specific test
pytest --cov=anthropic_client tests/       # Run with coverage
flake8 anthropic_client                    # Lint code
mypy anthropic_client                      # Type-check code
mypy src/python/anthropic_client           # Type-check all code in src
pre-commit run --all-files                 # Run all pre-commit hooks

# Narrative Isomorph package
cd src/python
python -m anthropic_client.narrative_isomorph.examples.advanced_analysis  # Run example
mcp build                                 # Build the project with MCP
mcp test                                  # Run tests with MCP

# Node.js / Claude Code CLI
npx claude-code                            # Run Claude Code CLI
```

## Code Style Guidelines

### Java
- Class names: PascalCase (e.g., `ModelArchitecture`)
- Methods/variables: camelCase (e.g., `computeScore()`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_SIZE`)
- Imports: standard library, third-party, project
- Include JavaDoc for public classes and methods
- Prefer constructor injection for Spring dependencies

### Python
- Follow PEP 8 and Black formatting (88 char line length)
- Function names: snake_case; Class names: PascalCase
- Imports order: standard library, third-party, local
- Use type hints and Google-style docstrings
- Use f-strings for string formatting
- Validate inputs and handle exceptions with meaningful messages
- Run pre-commit hooks before committing (black, isort, flake8, mypy)

### Narrative Isomorph Package
- Package path: `anthropic_client.narrative_isomorph`
- Core modules:
  - `representation.py`: Semantic representation of narratives
  - `calculus.py`: Isomorphism calculation between narratives
  - `interface.py`: Cross-architectural model interfaces
  - `temporal.py`: Multi-scale temporal analysis
  - `validation.py`: Statistical validation methods
  - `cultural.py`: Cross-cultural schema registry
  - `optimization.py`: Computational optimization
  - `ethics.py`: Ethical assessment framework
  - `pipeline.py`: Integration pipeline
  - `corpus.py`: Narrative corpus management
- Dependencies: sentence-transformers, numpy, networkx, nltk
- Examples in `examples/advanced_analysis.py`
- Tests in `/tests/narrative_isomorph/`

### JavaScript/Node.js
- Function names: camelCase; Constants: UPPER_SNAKE_CASE
- Use ES6+ features (arrow functions, destructuring)
- Prefer `const` over `let`, avoid `var`
- Handle async operations with async/await
- Use proper error handling with try/catch blocks

### Testing Best Practices
- Use descriptive test names that explain the scenario
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test both success and failure cases
- Include edge cases and boundary conditions