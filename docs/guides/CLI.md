# Anthropic Client CLI Documentation

This comprehensive guide explains how to use the Anthropic Client Command Line Interface (CLI) for interacting with Claude models from Anthropic and custom OpenAI models through our unified interface.

## Installation

Install the package to get access to the CLI:

```bash
# Using pip directly
cd /path/to/anthropic_project
pip install -e .

# Using Magic (recommended for Mojo support)
magic install
magic run pip install -e .
```

## Basic Usage

The CLI provides multiple ways to interact with AI models:

### Direct Prompts

Pass a prompt directly as a command-line argument:

```bash
# Using the Python module interface
python -m anthropic_client.cli "What is the capital of France?"

# Using the Mojo implementation
cd /path/to/anthropic_project/src/mojo/anthropic_client_mojo
./claudethinkstream "What is the capital of France?"
```

### Interactive Input

When you run the CLI without a prompt, it will switch to interactive mode:

```bash
python -m anthropic_client.cli
# Type your prompt...
# Press Enter twice to submit
```

### Pipe Mode

Read prompts from standard input:

```bash
echo "What is the meaning of life?" | python -m anthropic_client.cli
# or
cat prompt.txt | python -m anthropic_client.cli
```

## Command Options

### Core Options

```bash
python -m anthropic_client.cli [OPTIONS] [PROMPT]

Options:
  -ns, --no-stream     Disable streaming (streaming enabled by default)
  -t, --temperature    Set response temperature (0.0 to 1.0, default: 1.0)
  -m, --model          Select AI model
  -f, --format         Output format: text, json, markdown
  --system             Set system message/context
  --haiku              Generate response in haiku format
  --model-config       Path to custom model configuration
  -h, --help           Show help message
```

### Response Control

#### Streaming Mode
Responses are streamed by default. Disable streaming with:
```bash
python -m anthropic_client.cli -ns "Tell me a story"
python -m anthropic_client.cli --no-stream "Tell me a story"
```

#### Model Selection
Choose a specific model:
```bash
# Claude models
python -m anthropic_client.cli -m claude-3-5-haiku-20241022 "Quick question"
python -m anthropic_client.cli -m claude-3-7-sonnet-20250219 "Complex analysis"

# Custom OpenAI models (if configured)
python -m anthropic_client.cli -m gpt-4.5-preview-2025-02-27 "Compare LLM approaches"
python -m anthropic_client.cli -m o1-kob-o3 "Creative writing task"
```

#### Temperature Control
Adjust response randomness:
```bash
python -m anthropic_client.cli -t 0.2 "Solve this math problem"
python -m anthropic_client.cli -t 1.0 "Write a creative story"
```

#### Format Options
Control the output format:
```bash
python -m anthropic_client.cli -f json "List 5 capital cities"
python -m anthropic_client.cli -f markdown "Write documentation for a function"
```

## Enhanced Features

### System Messages
Set context or instructions for the model:
```bash
python -m anthropic_client.cli --system "You are a helpful math tutor." "Explain calculus"
```

### Haiku Mode
Get responses in haiku format:
```bash
python -m anthropic_client.cli --haiku "Describe the ocean"
```

### Custom Model Configurations
Use custom model definitions:
```bash
python -m anthropic_client.cli --model-config "/path/to/custom-model.json" "Your prompt"
```

## Environment Configuration

Control the CLI behavior through environment variables:

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required for Anthropic models)
- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI models)

These can be set in your `.env` file:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Examples

### Basic Examples

```bash
# Simple question with streaming (default)
python -m anthropic_client.cli "What is the theory of relativity?"

# Using the Haiku model for faster responses
python -m anthropic_client.cli -m claude-3-5-haiku-20241022 "What are the primary colors?"

# Generate a creative response
python -m anthropic_client.cli "Write a short poem about artificial intelligence"

# Get a structured JSON response
python -m anthropic_client.cli -f json "List 5 programming languages with their creator and year"

# Use the haiku mode
python -m anthropic_client.cli --haiku "Describe autumn leaves"
```

### Advanced Examples

```bash
# Technical analysis with system prompt
python -m anthropic_client.cli --system "You are an expert software engineer with deep knowledge of algorithms." "Explain the time complexity of quicksort"

# Deterministic factual response (low temperature)
python -m anthropic_client.cli -t 0.1 -m claude-3-7-sonnet-20250219 "List the planets in our solar system"

# Creative writing (high temperature)
python -m anthropic_client.cli -t 1.0 "Write a short science fiction story about AI"

# Process input from a file
cat article.txt | python -m anthropic_client.cli "Summarize this article in three bullet points"

# Using a custom model configuration
python -m anthropic_client.cli --model-config "custom-model.json" "Explain the difference between CNN and RNN"

# Using Mojo for improved performance
cd /path/to/anthropic_project/src/mojo/anthropic_client_mojo
./claudethinkstream "Explain quantum computing to a five-year-old"
```

### Use Cases

```bash
# Code explanation
python -m anthropic_client.cli "Explain what this code does:
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)"

# Data analysis
python -m anthropic_client.cli -f json "Convert this data to JSON:
Product, Price, Quantity
Laptop, 1200, 5
Phone, 800, 10
Tablet, 300, 15"

# Educational content
python -m anthropic_client.cli -m claude-3-7-sonnet-20250219 "Create a short lesson plan for teaching photosynthesis to middle school students"
```

```bash
# Simple question (with default streaming)
claudethink "What is the capital of France?"

# Multi-line input
claudethink "Please analyze this code:
def hello():
    print('Hello, World!')
"

# Disable streaming
claudethink -ns "Write a short story about a robot"

# Use Haiku model for faster responses
claudethink -m claude-3-5-haiku-20241022 "Quick fact check"

# Technical analysis with low temperature
claudethink -t 0.2 "Explain how TCP/IP works"

# With citations enabled (default)
claudethink "Explain quantum computing"
```

### Advanced Usage

```bash
# Pipe file contents
cat code.py | claudethink "Review this code and suggest improvements"

# Process multiple prompts
cat prompts.txt | while read prompt; do
    claudethink "$prompt" >> responses.txt
done

# Interactive session (with default streaming)
claudethink

# Use specific script for Haiku model
claudethinkhaiku "What's the fastest mammal?"
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

3. **Streaming Options**
   - Streaming is on by default for real-time responses
   - Disable streaming (-ns flag) for scripted usage
   - Use specialized scripts (claudethinkhaiku, etc.) for specific models

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