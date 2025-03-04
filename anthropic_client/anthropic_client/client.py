"""
Core client implementation for interacting with Anthropic's Claude models.
"""

import os
from typing import Optional, Iterator, Union
import anthropic
from dotenv import load_dotenv

class AnthropicClient:
    def __init__(self):
        load_dotenv()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def get_response(self, prompt: str, stream: bool = False, temperature: float = 1.0) -> Union[str, Iterator[str]]:
        """Get a response from Claude.
        
        Args:
            prompt: The user's prompt to send to Claude
            stream: Whether to stream the response
            temperature: Controls randomness in the response (0.0 to 1.0)
            
        Returns:
            Either a complete response string or an iterator of response chunks
        """
        message_params = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": 128000,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "thinking": {
                "type": "enabled",
                "budget_tokens": 128000
            },
            "betas": ["output-128k-2025-02-19"]
        }
        
        if stream:
            response = self.client.beta.messages.create(**message_params, stream=True)
            return (chunk.content[0].text for chunk in response)
        else:
            response = self.client.beta.messages.create(**message_params)
            return response.content[0].text 