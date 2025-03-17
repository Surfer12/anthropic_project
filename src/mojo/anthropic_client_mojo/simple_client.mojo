"""
Simplified client for Anthropic API that should compile without issues.
"""

import os
from python import Python, PythonObject

# Simple function to load environment variables
fn load_env() raises:
    var dotenv = Python.import_module("dotenv")
    _ = dotenv.load_dotenv()

# Main client function
fn generate_response(prompt: String) raises -> String:
    var anthropic = Python.import_module("anthropic")
    
    # Get API key from environment
    var os_module = Python.import_module("os")
    var environ = os_module.environ
    var api_key = String(environ.__getitem__("ANTHROPIC_API_KEY"))
    
    if len(api_key) == 0:
        return "Error: ANTHROPIC_API_KEY not set"
    
    # Create client using Python's string evaluation to avoid syntax issues
    var py_client = Python.evaluate("""
    import anthropic
    
    def create_client(api_key):
        return anthropic.Anthropic(api_key=api_key)
    
    create_client
    """)(api_key)
    
    # Create message
    var py_message = Python.evaluate("""
    def create_message(prompt):
        return [{"role": "user", "content": prompt}]
    create_message
    """)(prompt)
    
    # Generate response
    var py_response = Python.evaluate("""
    def generate(client, message, model="claude-3-opus-20240229"):
        try:
            response = client.beta.messages.create(
                model=model,
                max_tokens=4096,
                messages=message,
                temperature=0.7
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"
    
    generate
    """)(py_client, py_message)
    
    return String(py_response)

# Main function to test
fn main() raises:
    load_env()
    var response = generate_response("Hello, Claude!")
    print("Response: " + response) 