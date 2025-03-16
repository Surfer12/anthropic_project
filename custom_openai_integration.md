# Using JSON Configuration Files with Anthropic Client for Custom OpenAI Models

This document outlines how to leverage JSON configuration files within the Anthropic client to call custom OpenAI models.

## Overview

The Anthropic client can be extended to support custom OpenAI models by:
1. Creating model configuration JSON files
2. Modifying the client implementation to handle different model types
3. Loading model configurations dynamically

## Implementation Steps

### 1. JSON Configuration Structure

Based on the existing `o1-kob-o3.json` file, create similar configuration files for custom OpenAI models:

```json
{
  "model": "custom-openai-model-name",
  "model_provider": "openai",
  "max_tokens": 16000,
  "temperature": 0.7,
  "endpoint": "https://api.openai.com/v1/chat/completions",
  "headers": {
    "Authorization": "Bearer ${OPENAI_API_KEY}"
  },
  "parameters": {
    "thinking_enabled": false,
    "response_format": {
      "type": "json_object"
    }
  }
}
```

### 2. Extend ModelName Enum

Modify the `ModelName` enum in `client.py` to include custom OpenAI models:

```python
class ModelName(str, Enum):
    """Available model versions."""
    SONNET = "claude-3-7-sonnet-20250219"
    HAIKU = "claude-3-5-haiku-20241022"
    OPUS = "claude-3-opus-20240229"
    # Custom OpenAI models
    CUSTOM_GPT = "custom-openai-model-name"
    
    @property
    def provider(self) -> str:
        """Return the provider for this model."""
        openai_models = ["custom-openai-model-name"]
        return "openai" if self.value in openai_models else "anthropic"
```

### 3. Create a Model Configuration Loader

Create a new module to handle loading JSON model configurations:

```python
# model_config.py
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

def load_model_config(model_name: str) -> Optional[Dict[str, Any]]:
    """Load model configuration from JSON file.
    
    Args:
        model_name: The name of the model to load configuration for
        
    Returns:
        Dictionary containing model configuration or None if file not found
    """
    # Search in common locations for model configuration files
    config_locations = [
        Path(__file__).parent / f"{model_name}.json",
        Path(__file__).parent / "configs" / f"{model_name}.json",
        Path.home() / ".anthropic" / "configs" / f"{model_name}.json"
    ]
    
    for location in config_locations:
        if location.exists():
            with open(location, 'r') as f:
                return json.load(f)
                
    return None
```

### 4. Extend AnthropicClient to Support Multiple Providers

Modify the client implementation to handle both Anthropic and OpenAI models:

```python
class MultiProviderClient:
    """Client for interacting with multiple model providers."""
    
    def __init__(self) -> None:
        """Initialize the client with API keys from environment."""
        load_dotenv()
        
        # Initialize Anthropic client
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        if anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
            
        # Initialize OpenAI client
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            import openai
            openai.api_key = openai_api_key
            self.openai_client = openai
            
    def get_response(self, prompt: str, **kwargs):
        """Get response from appropriate model provider based on model name."""
        model = kwargs.get('model', ModelName.SONNET)
        if isinstance(model, str):
            model = ModelName(model)
            
        # Load custom model configuration if available
        model_config = load_model_config(model.value)
        
        if model.provider == "openai" or (model_config and model_config.get("model_provider") == "openai"):
            return self._get_openai_response(prompt, model_config, **kwargs)
        else:
            return self._get_anthropic_response(prompt, **kwargs)
            
    def _get_openai_response(self, prompt: str, model_config: Dict[str, Any], **kwargs):
        """Handle OpenAI API calls using model configuration."""
        # Implementation for OpenAI calls
        pass
        
    def _get_anthropic_response(self, prompt: str, **kwargs):
        """Handle Anthropic API calls."""
        # Existing implementation for Anthropic calls
        pass
```

### 5. CLI Integration

Update the CLI to support custom model configurations:

```python
# In cli.py
parser.add_argument(
    "--model-config",
    type=str,
    help="Path to a JSON file containing model configuration"
)

# In the main function
if args.model_config:
    with open(args.model_config, 'r') as f:
        model_config = json.load(f)
    # Use model_config to override defaults
```

## Usage Examples

### Command Line

```bash
# Using a custom OpenAI model with configuration file
python -m anthropic_client.cli --model-config models/custom-gpt4.json "Your prompt here"

# Using a predefined model name that maps to a custom configuration
python -m anthropic_client.cli -m custom-openai-model-name "Your prompt here"
```

### API Usage

```python
from anthropic_client.client import MultiProviderClient

client = MultiProviderClient()
response = client.get_response(
    "Your prompt here",
    model="custom-openai-model-name",
    temperature=0.7
)
```

## Security Considerations

1. Store API keys securely in environment variables
2. Never commit API keys to version control
3. Validate model configurations before use
4. Implement proper error handling for API failures

## Error Handling

Add robust error handling for different providers:

```python
try:
    if model.provider == "openai":
        # OpenAI-specific error handling
        response = self._get_openai_response(...)
    else:
        # Anthropic-specific error handling
        response = self._get_anthropic_response(...)
except Exception as e:
    logger.error(f"Error from {model.provider}: {str(e)}")
    raise
```