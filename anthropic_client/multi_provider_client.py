"""
Client for interacting with multiple model providers (Anthropic and OpenAI).
"""

import os
import json
import logging
from dotenv import load_dotenv
from typing import Any, Dict, Iterator, Union
import anthropic
from anthropic_client.client import ModelName, OutputFormat  # Assumes OutputFormat is defined in client.py
from anthropic_client.model_config import load_model_config

logger = logging.getLogger(__name__)

class MultiProviderClient:
    """Client for interacting with multiple model providers."""
    
    def __init__(self) -> None:
        """Initialize the client with API keys from the environment."""
        load_dotenv()
        
        # Initialize Anthropic client if API key is available
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        if anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        else:
            self.anthropic_client = None

        # Initialize OpenAI client if API key is available
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            import openai
            openai.api_key = openai_api_key
            self.openai_client = openai
        else:
            self.openai_client = None
            
    def get_response(self, prompt: str, **kwargs) -> Union[str, Iterator[str]]:
        """Get response from appropriate model provider based on model name.
        
        Args:
            prompt: The prompt to send.
            kwargs: Additional parameters including 'model', 'temperature', etc.
            
        Returns:
            The response from the model.
        """
        model = kwargs.get("model", ModelName.SONNET)
        if isinstance(model, str):
            model = ModelName(model)
            
        # Load custom model configuration if available
        model_config = load_model_config(model.value)
        
        if model.provider == "openai" or (model_config and model_config.get("model_provider") == "openai"):
            return self._get_openai_response(prompt, model_config, **kwargs)
        else:
            return self._get_anthropic_response(prompt, **kwargs)
            
    def _get_openai_response(self, prompt: str, model_config: Dict[str, Any], **kwargs) -> Any:
        """Handle OpenAI API calls using the given model configuration.
        
        Args:
            prompt: The prompt string.
            model_config: JSON configuration dictionary for the model.
            kwargs: Additional parameters such as temperature.
            
        Returns:
            The response from OpenAI.
        """
        # Example implementation using the OpenAI client with the given configuration
        if not self.openai_client:
            raise ValueError("OPENAI_API_KEY is not set")
        
        endpoint = model_config.get("endpoint")
        headers = model_config.get("headers", {})
        parameters = model_config.get("parameters", {})
        model_name = model_config.get("model")
        temperature = kwargs.get("temperature", model_config.get("temperature", 0.7))
        
        # This is a placeholder for making an API call to OpenAI's endpoint.
        try:
            response = self.openai_client.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                **parameters
            )
            return response.choices[0].message.get("content", "")
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}")
            raise

    def _get_anthropic_response(self, prompt: str, **kwargs) -> Any:
        """Handle Anthropic API calls."""
        if not self.anthropic_client:
            raise ValueError("ANTHROPIC_API_KEY is not set")
        # You may adapt the following according to your Anthropic client specifics.
        # For example, reuse the existing get_response logic from the AnthropicClient.
        try:
            message_params = {
                "model": kwargs.get("model", ModelName.SONNET).value,
                "max_tokens": kwargs.get("max_tokens", 128000),
                "temperature": kwargs.get("temperature", 1.0),
                "messages": [{"role": "user", "content": prompt}],
                "thinking": {"type": "enabled", "budget_tokens": 120000},
                "betas": ["output-128k-2025-02-19"],
                "citations": {"enabled": True}
            }
            
            if kwargs.get("stream", False):
                response = self.anthropic_client.beta.messages.create(**message_params, stream=True)
                return (chunk.content[0].text for chunk in response)
            else:
                response = self.anthropic_client.beta.messages.create(**message_params)
                return response.content[0].text
        except Exception as e:
            logger.error(f"Error calling Anthropic: {str(e)}")
            raise 