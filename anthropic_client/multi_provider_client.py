"""
Client for interacting with multiple model providers (Anthropic and OpenAI).
"""

import os
import json
import logging
from dotenv import load_dotenv
from typing import Any, Dict, Iterator, Union, List, Optional
import anthropic
from anthropic_client.client import ModelName, OutputFormat  # Assumes OutputFormat is defined in client.py
from anthropic_client.model_config import load_model_config

logger = logging.getLogger(__name__)

# Dictionary of known model capabilities
MODEL_CAPABILITIES = {
    "claude-3-5-haiku-20241022": {
        "supports_thinking": False,
        "supports_streaming": True
    },
    "claude-3-7-sonnet-20250219": {
        "supports_thinking": True,
        "supports_streaming": True
    },
    "claude-3-opus-20240229": {
        "supports_thinking": True,
        "supports_streaming": True
    }
}

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
        
        # Convert string to ModelName enum if it's a string
        if isinstance(model, str):
            try:
                model = ModelName(model)
            except ValueError:
                # If the string is not a valid enum value, just use it as is
                model_name = model
                # Default to anthropic provider if we can't determine
                model_provider = "anthropic"
                
                # Try to determine provider from the model name pattern
                if any(openai_model in model.lower() for openai_model in ["gpt", "o1-kob"]):
                    model_provider = "openai"
                
                # Create a simple object with value and provider attributes
                class SimpleModel:
                    def __init__(self, value, provider):
                        self.value = value
                        self.provider = provider
                
                model = SimpleModel(model_name, model_provider)
            
        # Load custom model configuration if available
        model_config = load_model_config(model.value)
        
        if model.provider == "openai" or (model_config and model_config.get("model_provider") == "openai"):
            return self._get_openai_response(prompt, model_config, **kwargs)
        else:
            return self._get_anthropic_response(prompt, **kwargs)
    
    def _check_model_capabilities(self, model_value: str) -> Dict[str, bool]:
        """Check the capabilities of a given model.
        
        Args:
            model_value: The model identifier string.
            
        Returns:
            Dictionary with capability flags.
        """
        # Default capabilities (assume most features are supported)
        default_capabilities = {
            "supports_thinking": True,
            "supports_streaming": True
        }
        
        # Return known capabilities or defaults
        return MODEL_CAPABILITIES.get(model_value, default_capabilities)
            
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
            # Handle the custom "responses" endpoint differently than standard OpenAI endpoints
            if endpoint and "/responses" in endpoint:
                import requests
                # Set up direct API request
                api_key = os.environ.get("OPENAI_API_KEY")
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                
                # Prepare request payload
                payload = {
                    "model": model_name,
                    "input": prompt,
                    **parameters
                }
                
                # Make direct API request
                response = requests.post(endpoint, headers=headers, json=payload)
                response_json = response.json()
                
                # Extract content from the response
                if response_json and "output" in response_json:
                    return response_json["output"]
                else:
                    logger.error(f"Invalid response format: {response_json}")
                    return "Error: Invalid response format"
            else:
                # Use standard OpenAI client for normal endpoints
                response = self.openai_client.ChatCompletion.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    **parameters
                )
                
                # Check if response and response.choices exist
                if not response or not hasattr(response, 'choices') or not response.choices:
                    logger.error("Invalid response format from OpenAI API")
                    return "Error: Invalid response format"
                    
                # Check if choice.message exists
                choice = response.choices[0]
                if not hasattr(choice, 'message') or not choice.message:
                    logger.error("Response missing message attribute")
                    return "Error: Response missing message attribute"
                    
                # Safely get content from message
                return choice.message.get("content", "")
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}")
            raise

    def _get_anthropic_response(self, prompt: str, **kwargs) -> Any:
        """Handle Anthropic API calls with capability detection and fallback."""
        if not self.anthropic_client:
            raise ValueError("ANTHROPIC_API_KEY is not set")
        
        # Get model and ensure we get the string value
        model = kwargs.get("model", ModelName.SONNET)
        model_value = model.value if hasattr(model, 'value') else model
        
        # Check model capabilities
        capabilities = self._check_model_capabilities(model_value)
        
        # Determine if we should use streaming
        use_streaming = kwargs.get("stream", False)
        
        # Determine if we should use thinking (based on model capabilities)
        use_thinking = capabilities["supports_thinking"]
        
        # Build base message parameters
        message_params = {
            "model": model_value,
            "max_tokens": kwargs.get("max_tokens", 128000),
            "temperature": kwargs.get("temperature", 1.0),
            "messages": [{"role": "user", "content": prompt}],
            "betas": ["output-128k-2025-02-19"]
        }
        
        # Add system message if provided
        if "system" in kwargs and kwargs["system"]:
            message_params["messages"].insert(0, {"role": "system", "content": kwargs["system"]})
        
        # Add thinking if supported and not explicitly disabled
        if use_thinking and kwargs.get("thinking", True):
            thinking_budget = kwargs.get("thinking_budget", 120000)
            message_params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
        
        # Try streaming if requested and supported
        if use_streaming and capabilities["supports_streaming"]:
            try:
                return self._stream_anthropic_response(message_params)
            except Exception as e:
                logger.warning(f"Streaming failed, falling back to non-streaming: {str(e)}")
                # Fall back to non-streaming
                return self._batch_anthropic_response(message_params)
        else:
            # Use non-streaming by default
            return self._batch_anthropic_response(message_params)
    
    def _stream_anthropic_response(self, message_params: Dict[str, Any]) -> Iterator[str]:
        """Handle streaming Anthropic API calls.
        
        Args:
            message_params: The message parameters to send.
            
        Returns:
            An iterator of response chunks.
        """
        try:
            response = self.anthropic_client.beta.messages.create(**message_params, stream=True)
            # Extract text from each chunk's content
            return (chunk.delta.text for chunk in response if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'))
        except Exception as e:
            logger.error(f"Error in streaming response: {str(e)}")
            raise
    
    def _batch_anthropic_response(self, message_params: Dict[str, Any]) -> str:
        """Handle non-streaming (batch) Anthropic API calls.
        
        Args:
            message_params: The message parameters to send.
            
        Returns:
            The complete response as a string.
        """
        try:
            response = self.anthropic_client.beta.messages.create(**message_params)
            # Extract text from the response content
            if hasattr(response, 'content') and len(response.content) > 0:
                return response.content[0].text
            return ""
        except Exception as e:
            logger.error(f"Error in batch response: {str(e)}")
            raise 