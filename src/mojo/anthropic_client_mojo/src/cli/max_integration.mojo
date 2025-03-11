"""
Max Integration Module for Anthropic Claude API Client

This module provides advanced integration capabilities between 
the Anthropic Claude API and Max computational environments.
"""

from python import Python, PythonObject
from client import AnthropicClient, ClientConfig

@value
struct MaxAnthropicIntegration:
    var client: AnthropicClient
    
    fn __init__(mut self, api_key: String = "") raises:
        """
        Initialize Max-Anthropic integration with optional API key.
        
        Args:
            api_key: Optional API key for Anthropic. 
                     If not provided, will attempt to load from environment.
        """
        if len(api_key) > 0:
            self.client = AnthropicClient(ClientConfig(
                api_key=api_key, 
                model="claude-3-opus-20240229",  # Default to most advanced model
                max_tokens=256000,  # Increased max tokens for Max integration
                temperature=0.7  # Slightly more creative default
            ))
        else:
            self.client = AnthropicClient()
    
    fn process_max_prompt(self, prompt: String, max_context: PythonObject = None) raises -> String:
        """
        Process a prompt with optional Max computational context.
        
        Args:
            prompt: The primary text prompt.
            max_context: Optional Python object representing Max computational context.
        
        Returns:
            Processed response from Claude.
        """
        # Enhance prompt with Max context if provided
        var enhanced_prompt = prompt
        if max_context is not None:
            var context_description = str(max_context)
            enhanced_prompt = "Max Computational Context: " + context_description + "\n\n" + prompt
        
        return self.client.get_response(enhanced_prompt)
    
    fn stream_max_response(self, prompt: String, max_context: PythonObject = None) raises -> PythonObject:
        """
        Stream a response with optional Max computational context.
        
        Args:
            prompt: The primary text prompt.
            max_context: Optional Python object representing Max computational context.
        
        Returns:
            Streaming response iterator.
        """
        # Enhance prompt with Max context if provided
        var enhanced_prompt = prompt
        if max_context is not None:
            var context_description = str(max_context)
            enhanced_prompt = "Max Computational Context: " + context_description + "\n\n" + prompt
        
        return self.client.get_response(enhanced_prompt, stream=True)
    
    fn analyze_max_data(self, data: PythonObject) raises -> String:
        """
        Analyze Max computational data using Claude.
        
        Args:
            data: Python object representing computational data.
        
        Returns:
            Analytical insights from Claude.
        """
        var data_description = str(data)
        var prompt = """
        Analyze the following Max computational data:
        
        Data Structure: {data_description}
        
        Provide insights on:
        1. Computational characteristics
        2. Potential optimization strategies
        3. Algorithmic complexity analysis
        """
        
        return self.client.get_response(prompt) 