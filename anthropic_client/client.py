"""
Core client implementation for interacting with Anthropic's Claude models.
"""

import os
from enum import Enum
from typing import Optional, Iterator, Union, List, Dict, Any
import anthropic
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelName(str, Enum):
    """Available Claude model versions."""
    SONNET = "claude-3-7-sonnet-20250219"
    HAIKU = "claude-3-5-haiku-20241022"
    OPUS = "claude-3-opus-20240229"
    # Custom OpenAI models
    CUSTOM_GPT = "custom-openai-model-name"
    O1_KOB_O3 = "o1-kob-o3"
    GPT_4_5 = "gpt-4.5-preview-2025-02-27"

    @property
    def provider(self) -> str:
        """Return the provider for this model."""
        openai_models = ["custom-openai-model-name", "o1-kob-o3", "gpt-4.5-preview-2025-02-27"]
        return "openai" if self.value in openai_models else "anthropic"

class OutputFormat(str, Enum):
    """Available output formats."""
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"

class AnthropicClient:
    """Client for interacting with Anthropic's Claude models."""
    
    MAX_TOKENS: int = 128000
    THINKING_BUDGET: int = 120000
    MIN_TEMPERATURE: float = 0.0
    MAX_TEMPERATURE: float = 1.0
    
    def __init__(self) -> None:
        """Initialize the Anthropic client with API key from environment."""
        load_dotenv()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def _validate_temperature(self, temperature: float) -> None:
        """Validate that temperature is within allowed range."""
        if not self.MIN_TEMPERATURE <= temperature <= self.MAX_TEMPERATURE:
            raise ValueError(
                f"Temperature must be between {self.MIN_TEMPERATURE} and {self.MAX_TEMPERATURE}"
            )
    
    def _build_message_params(
        self,
        prompt: str,
        temperature: float,
        model: ModelName,
        format: OutputFormat,
        system: Optional[str]
    ) -> Dict[str, Any]:
        """Build the message parameters for the API request."""
        messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
        if system:
            messages.insert(0, {"role": "system", "content": system})
            
        params = {
            "model": model.value,
            "max_tokens": self.MAX_TOKENS,
            "temperature": temperature,
            "messages": messages,
            "thinking": {
                "type": "enabled",
                "budget_tokens": self.THINKING_BUDGET
            },
            "betas": ["output-128k-2025-02-19"],
            "citations": {"enabled": True}
        }
        
        if format == OutputFormat.JSON:
            params["response_format"] = {"type": "json_object"}
            
        return params
        
    def get_response(
        self,
        prompt: str,
        stream: bool = False,
        temperature: float = 1.0,
        model: Union[str, ModelName] = ModelName.SONNET,
        format: Union[str, OutputFormat] = OutputFormat.TEXT,
        system: Optional[str] = None
    ) -> Union[str, Iterator[str]]:
        """Get a response from Claude.
        
        Args:
            prompt: The user's prompt to send to Claude
            stream: Whether to stream the response
            temperature: Controls randomness in the response (0.0 to 1.0)
            model: The Claude model to use
            format: Output format (text, json, markdown)
            system: Optional system prompt to set context/permissions
            
        Returns:
            Either a complete response string or an iterator of response chunks
            
        Raises:
            ValueError: If temperature is out of range or other validation fails
        """
        # Convert string enums to proper enum types if needed
        if isinstance(model, str):
            model = ModelName(model)
        if isinstance(format, str):
            format = OutputFormat(format)
            
        self._validate_temperature(temperature)
        
        try:
            message_params = self._build_message_params(
                prompt, temperature, model, format, system
            )
            
            if stream:
                response = self.client.beta.messages.create(**message_params, stream=True)
                return (chunk.content[0].text for chunk in response)
            else:
                response = self.client.beta.messages.create(**message_params)
                return response.content[0].text
                
        except Exception as e:
            logger.error(f"Error getting response from Claude: {str(e)}")
            raise 