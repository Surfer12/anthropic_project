# Command Line Interface (CLI) Documentation

The `claudethink` command line interface provides a convenient way to interact with the Anthropic Claude API directly from your terminal.

## Installation

The CLI is automatically installed when you install the package:

```bash
# Using Magic (recommended)
magic install
magic run pip install -e .

# Using pip directly
pip install .
```

## Basic Usage

The CLI supports several modes of operation:

### Direct Prompts

Send a prompt directly as a command line argument:

```bash
claudethink "What is the capital of France?"
```

### Interactive Mode

Launch an interactive session where you can type multi-line prompts:

```bash
claudethink
# Type your prompt...
# Press Ctrl+D (Unix) or Ctrl+Z (Windows) to submit
```

### Pipe Mode

Read prompts from standard input:

```bash
echo "What is the meaning of life?" | claudethink
# or
cat prompt.txt | claudethink
```

## Command Options

### Core Options

```bash
claudethink [OPTIONS] [PROMPT]

Options:
  -s, --stream       Stream the response in real-time
  -t, --temperature  Set response temperature (0.0 to 1.0, default: 1.0)
  -b, --budget      Set thinking budget in tokens (1 to 128000, default: 128000)
  -h, --help        Show this help message
  -v, --version     Show version information
```

### Response Control

#### Streaming Mode
Enable real-time streaming of responses:
```bash
claudethink -s "Tell me a story"
```

#### Temperature Control
Adjust response randomness (lower values = more focused):
```bash
claudethink -t 0.2 "Solve this math problem"
claudethink --temperature 0.8 "Write a creative story"
```

#### Thinking Budget
Control the token budget for thinking:
```bash
claudethink -b 64000 "Summarize this text"
claudethink --budget 32000 "Quick analysis"
```

## Environment Configuration

The CLI respects the following environment variables:

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `CLAUDE_MODEL`: Override default model (optional)
- `CLAUDE_TEMPERATURE`: Default temperature (optional)
- `CLAUDE_THINKING_BUDGET`: Default thinking budget (optional)

These can be set in your `.env` file:
```bash
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-7-sonnet-20250219
CLAUDE_TEMPERATURE=0.7
CLAUDE_THINKING_BUDGET=64000
```

## Examples

### Basic Examples

```bash
# Simple question
claudethink "What is the capital of France?"

# Multi-line input
claudethink "Please analyze this code:
def hello():
    print('Hello, World!')
"

# Stream a long response
claudethink -s "Write a short story about a robot"

# Technical analysis with low temperature
claudethink -t 0.2 "Explain how TCP/IP works"
```

### Advanced Usage

```bash
# Pipe file contents
cat code.py | claudethink "Review this code and suggest improvements"

# Process multiple prompts
cat prompts.txt | while read prompt; do
    claudethink "$prompt" >> responses.txt
done

# Interactive session with streaming
claudethink -s
```

## Error Handling

The CLI provides clear error messages for common issues:

- Missing API key
- Invalid temperature values
- Network connectivity problems
- API rate limiting
- Invalid prompts
- Insufficient thinking budget

Example error messages:
```bash
Error: ANTHROPIC_API_KEY environment variable not set
Error: Temperature must be between 0.0 and 1.0
Error: API request failed: rate limit exceeded
```

## Best Practices

1. **Use Temperature Appropriately**
   - Low (0.1-0.3) for factual/analytical tasks
   - Medium (0.4-0.7) for balanced responses
   - High (0.8-1.0) for creative tasks

2. **Optimize Thinking Budget**
   - Use lower budgets for simple queries
   - Increase budget for complex analysis
   - Monitor token usage in responses

3. **Leverage Streaming**
   - Enable streaming for long responses
   - Use streaming for interactive applications
   - Consider disabling for scripted usage

4. **Input Handling**
   - Use quotes for prompts with spaces
   - Use heredocs for multi-line input
   - Consider file input for long prompts

## Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Ensure ANTHROPIC_API_KEY is set
   - Check key validity
   - Verify environment file loading

2. **Rate Limiting**
   - Implement backoff in scripts
   - Monitor usage patterns
   - Consider batch processing

3. **Network Problems**
   - Check internet connectivity
   - Verify proxy settings
   - Ensure API endpoint access

4. **Response Issues**
   - Verify prompt formatting
   - Check temperature settings
   - Monitor thinking budget

## Support

For additional help:
- Check the project README
- Review CLAUDE.md for development guidelines
- Submit issues on the project repository
- Contact the maintainers 