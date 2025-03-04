"""
Test suite for the Anthropic Claude API Mojo client.
"""

from python import Python
from client import AnthropicClient, get_env, load_dotenv

fn test_env_loading() raises:
    print("Testing environment loading...")
    load_dotenv()
    var api_key = get_env("ANTHROPIC_API_KEY")
    if len(api_key) == 0:
        raise Error("API key not found in environment")
    print("✓ Environment loading test passed")

fn test_client_initialization() raises:
    print("Testing client initialization...")
    var client = AnthropicClient()
    if client.client is None:
        raise Error("Client initialization failed")
    print("✓ Client initialization test passed")

fn test_response_generation() raises:
    print("Testing response generation...")
    var client = AnthropicClient()
    
    # Test basic response
    var test_prompt = "Say 'test successful' and nothing else"
    var response = client.get_response(test_prompt, False, 0.0)
    var response_text = String(response).lower()
    if "test successful" not in response_text:
        raise Error("Response did not contain expected text")
    print("✓ Basic response test passed")
    
    # Test temperature validation
    var error_caught = False
    try:
        _ = client.get_response("test", False, 1.5)
    except:
        error_caught = True
    if not error_caught:
        raise Error("Temperature validation failed")
    print("✓ Temperature validation test passed")
    
    # Test empty prompt validation
    error_caught = False
    try:
        _ = client.get_response("   ", False, 1.0)
    except:
        error_caught = True
    if not error_caught:
        raise Error("Empty prompt validation failed")
    print("✓ Empty prompt validation test passed")

fn test_streaming() raises:
    print("Testing streaming...")
    var client = AnthropicClient()
    var test_prompt = "Count from 1 to 3"
    var stream_response = client.get_response(test_prompt, True, 0.0)
    
    var has_content = False
    for chunk in stream_response:
        has_content = True
        break
    
    if not has_content:
        raise Error("Stream did not produce any content")
    print("✓ Streaming test passed")

fn run_tests() raises:
    print("\n=== Running Anthropic Client Tests ===\n")
    
    test_env_loading()
    test_client_initialization()
    test_response_generation()
    test_streaming()
    
    print("\n✓ All tests completed successfully!\n")

fn main() raises:
    run_tests() 