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
    
    fn __init__(mut self, api_key: String, 
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
    
    # Make the struct convertible to a PythonObject
    fn __python__(self) raises -> PythonObject:
        # Create a Python wrapper to ensure proper conversion
        var py_wrapper = Python.evaluate("""
        class MojoClientWrapper:
            def __init__(self, client_obj):
                self.client = client_obj
            
            def get_response(self, prompt, stream=False, temperature=1.0):
                # This function will be called from Python
                import anthropic
                
                api_key = client_obj.config.api_key
                model = client_obj.config.model
                max_tokens = client_obj.config.max_tokens
                thinking_budget = client_obj.config.thinking_budget
                
                try:
                    anthropic_client = anthropic.Anthropic(api_key=api_key)
                    
                    thinking = {"type": "enabled", "budget_tokens": thinking_budget}
                    betas = ["output-128k-2025-02-19"]
                    
                    if stream:
                        return anthropic_client.beta.messages.create(
                            model=model,
                            max_tokens=max_tokens,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature,
                            thinking=thinking,
                            betas=betas,
                            stream=True
                        )
                    else:
                        response = anthropic_client.beta.messages.create(
                            model=model,
                            max_tokens=max_tokens,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature,
                            thinking=thinking,
                            betas=betas
                        )
                        return response.content[0].text
                except Exception as e:
                    raise Exception(f"Error calling Anthropic API: {e}")
                
        MojoClientWrapper
        """)
        
        # Create a python representation of our config values
        var py_config = Python.dict()
        py_config["api_key"] = self.config.api_key
        py_config["model"] = self.config.model
        py_config["max_tokens"] = self.config.max_tokens
        py_config["thinking_budget"] = self.config.thinking_budget
        
        # Return a Python object that wraps this client
        return py_wrapper(py_config)
    
    fn __init__(mut self) raises:
        load_dotenv()
        var api_key = get_env("ANTHROPIC_API_KEY")
        if len(api_key) == 0:
            raise Error("ANTHROPIC_API_KEY environment variable not set")
        
        self.config = ClientConfig(api_key)
        var anthropic = Python.import_module("anthropic")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    fn get_response(self, prompt: String, stream: Bool = False, temperature: Float64 = 1.0) raises -> PythonObject:
        """
        The prompt to send to Claude.
        Args:
            prompt: The text prompt to send to Claude.
            stream: Whether to stream the response.
            temperature: Controls randomness in the response (0-1).
        """
        # Input validation with early returns
        if temperature < 0.0 or temperature > 1.0:
            raise Error("Temperature must be between 0.0 and 1.0")
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
            temperature, 
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