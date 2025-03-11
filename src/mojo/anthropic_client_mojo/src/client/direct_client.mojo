"""
Optimized Anthropic Client Implementation with Direct Python API Integration

This module provides a high-performance Anthropic client implementation
that uses direct Python API calls instead of string-based evaluation.
"""

import os
from python import Python, PythonObject
from sys.info import sizeof

# Import the anthropic module directly at module load time
var anthropic_module = Python.import_module("anthropic")
var dotenv_module = Python.import_module("dotenv")

# Load environment variables at module initialization
_ = dotenv_module.load_dotenv()

@value
struct DirectClientConfig:
    var api_key: String
    var model: String
    var max_tokens: Int
    var thinking_budget: Int
    var temperature: Float64
    
    fn __init__(mut self, api_key: String, 
                model: String = "claude-3-sonnet-20250219",
                max_tokens: Int = 128000,
                thinking_budget: Int = 120000,
                temperature: Float64 = 1.0):
        # Input validation
        if temperature < 0.0 or temperature > 1.0:
            raise Error("Temperature must be between 0.0 and 1.0")
        
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.thinking_budget = thinking_budget
        self.temperature = temperature

@value
struct DirectResponseMetrics:
    var start_time: Int64
    var end_time: Int64
    var total_tokens: Int
    var latency_ms: Float64
    
    fn __init__(mut self):
        self.start_time = 0  # TODO: Implement proper timing
        self.end_time = 0
        self.total_tokens = 0
        self.latency_ms = 0.0
    
    fn complete(mut self, tokens: Int):
        self.end_time = 0  # TODO: Implement proper timing
        self.total_tokens = tokens
        self.latency_ms = 0.0  # TODO: Calculate actual latency

@value
struct DirectAnthropicClient:
    var client: PythonObject
    var config: DirectClientConfig
    
    fn __init__(mut self, config: DirectClientConfig) raises:
        """
        Initialize client with direct Python API integration.
        
        Args:
            config: Client configuration
        """
        self.config = config
        
        # Create Anthropic client directly using imported module
        self.client = anthropic_module.Anthropic(api_key=config.api_key)
    
    fn __init__(mut self) raises:
        """
        Initialize client with API key from environment.
        """
        var os_module = Python.import_module("os")
        var environ = os_module.environ
        
        # Get API key from environment
        var api_key_obj = environ.get("ANTHROPIC_API_KEY")
        if api_key_obj is None:
            raise Error("ANTHROPIC_API_KEY environment variable not set")
        
        var api_key = String(api_key_obj)
        if len(api_key) == 0:
            raise Error("ANTHROPIC_API_KEY environment variable is empty")
        
        self.config = DirectClientConfig(api_key)
        
        # Create Anthropic client directly using imported module
        self.client = anthropic_module.Anthropic(api_key=api_key)
    
    fn get_response(self, prompt: String, stream: Bool = False) raises -> PythonObject:
        """
        Get response from Claude using direct Python API calls.
        
        Args:
            prompt: Input prompt text
            stream: Whether to stream the response
        
        Returns:
            Response object or stream
        """
        # Input validation
        if len(prompt.strip()) == 0:
            raise Error("Prompt cannot be empty")
        
        var metrics = DirectResponseMetrics()
        
        # Create messages list directly
        var messages_list = Python.list()
        var message = Python.dict()
        message["role"] = "user"
        message["content"] = prompt
        messages_list.append(message)
        
        # Create thinking parameter
        var thinking = Python.dict()
        thinking["type"] = "enabled"
        thinking["budget_tokens"] = self.config.thinking_budget
        
        # Create betas list
        var betas = Python.list()
        betas.append("output-128k-2025-02-19")
        
        # Access messages API directly
        var messages_api = self.client.beta.messages
        
        # Create parameters dictionary
        var params = Python.dict()
        params["model"] = self.config.model
        params["max_tokens"] = self.config.max_tokens
        params["messages"] = messages_list
        params["temperature"] = self.config.temperature
        params["thinking"] = thinking
        params["betas"] = betas
        
        if stream:
            params["stream"] = True
        
        # Direct API call using Python.call
        var response = Python.call(messages_api.create, **params)
        
        if stream:
            return response
        else:
            # Update metrics
            var output_tokens = response.usage.output_tokens
            metrics.complete(Int(output_tokens))
            
            # Extract and return content
            return response.content[0].text
    
    fn stream_response(self, prompt: String) raises -> PythonObject:
        """
        Stream response from Claude using direct Python API calls.
        
        Args:
            prompt: Input prompt text
        
        Returns:
            Streaming response iterator
        """
        return self.get_response(prompt, stream=True)
    
    fn process_stream(self, stream: PythonObject) raises:
        """
        Process a streaming response.
        
        Args:
            stream: Streaming response iterator
        """
        var sys_module = Python.import_module("sys")
        var stdout = sys_module.stdout
        
        # Iterate through stream chunks
        for chunk in stream:
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                var chunk_text = String(chunk.delta.text)
                if len(chunk_text) > 0:
                    stdout.write(chunk_text)
                    stdout.flush()
        
        stdout.write("\n")
        stdout.flush()

# Utility function to get environment variable
fn get_env_direct(name: String) raises -> String:
    """
    Get environment variable using direct Python API calls.
    
    Args:
        name: Environment variable name
    
    Returns:
        Environment variable value
    """
    var os_module = Python.import_module("os")
    var environ = os_module.environ
    var value = environ.get(name)
    
    if value is None:
        return ""
    
    return String(value)

# Example usage function
fn example_direct_usage() raises:
    """Example of using the direct API client."""
    # Get API key from environment
    var api_key = get_env_direct("ANTHROPIC_API_KEY")
    if len(api_key) == 0:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return
    
    # Create client with direct API integration
    var client = DirectAnthropicClient(DirectClientConfig(
        api_key=api_key,
        model="claude-3-sonnet-20250219",
        temperature=0.7
    ))
    
    # Get response using direct API call
    var prompt = "Explain quantum computing in simple terms."
    var response = client.get_response(prompt)
    
    # Print response
    print("Claude: " + String(response))
    
    # Example of streaming response
    print("\nStreaming response:")
    var stream = client.stream_response("What are three interesting facts about space?")
    client.process_stream(stream) 