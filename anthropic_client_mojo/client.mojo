"""
Core client implementation for interacting with Anthropic's Claude models.
Optimized Mojo version of the original Python client.
"""

import os
from python import Python
from python.object import PythonObject
from sys.info import sizeof
from memory import unsafe_memset_zero

@value
struct ClientConfig:
    var api_key: String
    var model: String
    var max_tokens: Int
    var thinking_budget: Int
    
    fn __init__(inout self, api_key: String, 
                model: String = "claude-3-7-sonnet-20250219",
                max_tokens: Int = 128000,
                thinking_budget: Int = 120000):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.thinking_budget = thinking_budget

fn load_dotenv() raises:
    var dotenv = Python.import_module("dotenv")
    _ = dotenv.load_dotenv()

fn get_env(name: String) raises -> String:
    var os_module = Python.import_module("os")
    var environ = os_module.environ
    var value = environ.__getitem__(name)
    return String(value)

@value
struct ResponseMetrics:
    var start_time: Int64
    var end_time: Int64
    var total_tokens: Int
    
    fn __init__(inout self):
        self.start_time = 0  # TODO: Implement proper timing when available
        self.end_time = 0
        self.total_tokens = 0
    
    fn complete(inout self, tokens: Int):
        self.end_time = 0  # TODO: Implement proper timing when available
        self.total_tokens = tokens
    
    fn duration_ms(self) -> Float64:
        return 0.0  # TODO: Implement proper timing when available

struct AnthropicClient:
    var client: PythonObject
    var config: ClientConfig
    
    fn __init__(inout self) raises:
        load_dotenv()
        var api_key = get_env("ANTHROPIC_API_KEY")
        if len(api_key) == 0:
            raise Error("ANTHROPIC_API_KEY environment variable not set")
        
        self.config = ClientConfig(api_key)
        var anthropic = Python.import_module("anthropic")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    fn get_response(self, prompt: String, stream: Bool = False, temperature: Float64 = 1.0) raises -> PythonObject:
        """Get a response from Claude with performance metrics.
        
        Args:
            prompt: The user's prompt to send to Claude
            stream: Whether to stream the response
            temperature: Controls randomness in the response (0.0 to 1.0)
            
        Returns:
            Either a complete response string or an iterator of response chunks
        """
        # Input validation with early returns
        if temperature < 0.0 or temperature > 1.0:
            raise Error("Temperature must be between 0.0 and 1.0")
        if len(prompt.strip()) == 0:
            raise Error("Prompt cannot be empty")
        
        var metrics = ResponseMetrics()
        
        # Build message parameters efficiently
        var message_params = Python.dict()
        message_params["model"] = self.config.model
        message_params["max_tokens"] = self.config.max_tokens
        message_params["temperature"] = temperature
        
        var messages = Python.list()
        var message = Python.dict()
        message["role"] = "user"
        message["content"] = prompt
        messages.append(message)
        message_params["messages"] = messages
        
        var thinking = Python.dict()
        thinking["type"] = "enabled"
        thinking["budget_tokens"] = self.config.thinking_budget
        message_params["thinking"] = thinking
        
        var betas = Python.list()
        betas.append("output-128k-2025-02-19")
        message_params["betas"] = betas
        
        if stream:
            message_params["stream"] = True
            var response = self.client.beta.messages.create(**message_params)
            return response
        else:
            var response = self.client.beta.messages.create(**message_params)
            # Update metrics before returning
            metrics.complete(int(response.usage.output_tokens))
            return response.content[0].text
    
    fn __del__(owned self):
        """Clean up resources."""
        unsafe_memset_zero(self)