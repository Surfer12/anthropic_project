"""
Core client implementation for interacting with Anthropic's Claude models.
Mojo version of the original Python client.
"""

import os
from python import Python
from python.object import PythonObject

fn load_dotenv() raises:
    let dotenv = Python.import_module("dotenv")
    _ = dotenv.load_dotenv()

fn get_env(name: String) raises -> String:
    let os_module = Python.import_module("os")
    let environ = os_module.environ
    let value = environ.__getitem__(name)
    return String(value)

struct AnthropicClient:
    var client: PythonObject
    
    fn __init__(inout self) raises:
        load_dotenv()
        let api_key = get_env("ANTHROPIC_API_KEY")
        if len(api_key) == 0:
            raise Error("ANTHROPIC_API_KEY environment variable not set")
        
        let anthropic = Python.import_module("anthropic")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    fn get_response(self, prompt: String, stream: Bool = False, temperature: Float64 = 1.0) raises -> PythonObject:
        """Get a response from Claude.
        
        Args:
            prompt: The user's prompt to send to Claude
            stream: Whether to stream the response
            temperature: Controls randomness in the response (0.0 to 1.0)
            
        Returns:
            Either a complete response string or an iterator of response chunks
        """
        # Validate temperature
        if temperature < 0.0 or temperature > 1.0:
            raise Error("Temperature must be between 0.0 and 1.0")
        
        # Validate prompt
        if len(prompt.strip()) == 0:
            raise Error("Prompt cannot be empty")
        
        let message_params = Python.dict()
        message_params["model"] = "claude-3-7-sonnet-20250219"
        message_params["max_tokens"] = 128000
        message_params["temperature"] = temperature
        
        let messages = Python.list()
        let message = Python.dict()
        message["role"] = "user"
        message["content"] = prompt
        messages.append(message)
        message_params["messages"] = messages
        
        let thinking = Python.dict()
        thinking["type"] = "enabled"
        thinking["budget_tokens"] = 120000
        message_params["thinking"] = thinking
        
        let betas = Python.list()
        betas.append("output-128k-2025-02-19")
        message_params["betas"] = betas
        
        if stream:
            message_params["stream"] = True
            let response = self.client.beta.messages.create(**message_params)
            return response
        else:
            let response = self.client.beta.messages.create(**message_params)
            return response.content[0].text