"""
Core client implementation for interacting with Anthropic's Claude models.
Optimized Mojo version of the original Python client.
"""

import os
from python import Python, PythonObject
from sys.info import sizeof

@value
struct ClientConfig:
    var api_key: String
    var model: String
    var max_tokens: Int
    var thinking_budget: Int
    var temperature: Float64
    
    fn __init__(mut self, api_key: String, 
                model: String = "claude-3-opus-20240229",
                temperature: Float64 = 0.7,
                max_tokens: Int = 4096,
                thinking_budget: Int = 2000) raises:
        # Add input validation
        if temperature < 0.0 or temperature > 1.0:
            raise Error("Temperature must be between 0.0 and 1.0")
        
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.thinking_budget = thinking_budget
        self.temperature = temperature

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
    
    fn __init__(mut self):
        self.start_time = 0  # TODO: Implement proper timing when available
        self.end_time = 0
        self.total_tokens = 0
    
    fn complete(mut self, tokens: Int):
        self.end_time = 0  # TODO: Implement proper timing when available
        self.total_tokens = tokens
    
    fn duration_ms(self) -> Float64:
        return 0.0  # TODO: Implement proper timing when available

@value
struct AnthropicClient:
    var client: PythonObject
    var config: ClientConfig
    
    fn get_python_response(self, prompt: String) raises -> PythonObject:
        """
        Direct Python API method for response generation.
        
        Args:
            prompt: Input text prompt
        
        Returns:
            Python response object
        """
        var anthropic_py = Python.import_module("anthropic")
        var client_py = anthropic_py.Anthropic(api_key=self.config.api_key)
        
        var messages_list = Python.list()
        var message = Python.dict()
        message["role"] = "user"
        message["content"] = prompt
        messages_list.append(message)
        
        var response_params = Python.dict()
        response_params["model"] = self.config.model
        response_params["max_tokens"] = self.config.max_tokens
        response_params["messages"] = messages_list
        response_params["temperature"] = self.config.temperature
        
        # Create a separate Python dictionary for thinking params
        var thinking_params = Python.dict()
        thinking_params["type"] = "enabled"
        thinking_params["budget_tokens"] = self.config.thinking_budget
        
        # Assign it to the response_params
        response_params["thinking"] = thinking_params
        
        response_params["betas"] = ["output-128k-2025-02-19"]
        
        # Direct Python function call
        var response_py = client_py.beta.messages.create(**response_params)
        
        return response_py

    fn __python__(self) raises -> PythonObject:
        """
        Simplified Python conversion method leveraging direct API call.
        
        Returns:
            Python-compatible wrapper object
        """
        var py_wrapper = Python.evaluate("""
        class MojoClientWrapper:
            def __init__(self, mojo_client):
                self.mojo_client = mojo_client
            
            def get_response(self, prompt, stream=False):
                return self.mojo_client.get_python_response(prompt)
        
        MojoClientWrapper
        """)
    
    fn __init__(mut self) raises:
        load_dotenv()
        var api_key = get_env("ANTHROPIC_API_KEY")
        if len(api_key) == 0:
            raise Error("ANTHROPIC_API_KEY environment variable not set")
        
        self.config = ClientConfig(api_key)
        var anthropic = Python.import_module("anthropic")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    fn get_response(self, prompt: String, stream: Bool = False) raises -> PythonObject:
        """
        The prompt to send to Claude.
        Args:
            prompt: The text prompt to send to Claude.
            stream: Whether to stream the response.
        """
        # Input validation with early returns
        if len(prompt.strip()) == 0:
            raise Error("Prompt cannot be empty")
        
        var metrics = ResponseMetrics()
        
        # Use Python's create_message function pattern to avoid ** syntax issues
        var messages_list = Python.list()
        var message = Python.dict()
        message["role"] = "user"
        message["content"] = prompt
        messages_list.append(message)
        
        # Create a Python function to handle the call
        var py_func = Python.evaluate("""
        def call_anthropic(client, model, max_tokens, messages, temperature, stream, thinking_budget):
            thinking = {"type": "enabled", "budget_tokens": thinking_budget}
            betas = ["output-128k-2025-02-19"]
            
            if stream:
                return client.beta.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=messages,
                    temperature=temperature,
                    thinking=thinking,
                    betas=betas,
                    stream=True
                )
            else:
                response = client.beta.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=messages,
                    temperature=temperature,
                    thinking=thinking,
                    betas=betas
                )
                return response
        
        call_anthropic
        """)
        
        var response = py_func(
            self.client, 
            self.config.model, 
            self.config.max_tokens, 
            messages_list, 
            self.config.temperature,  # Use configuration temperature 
            stream, 
            self.config.thinking_budget
        )
        
        if stream:
            return response
        else:
            # Update metrics before returning
            metrics.complete(Int(response.usage.output_tokens))
            return response.content[0].text
    
    fn __del__(owned self):
        """Clean up resources."""
        # Resource cleanup (no unsafe_memset_zero in newer Mojo versions)