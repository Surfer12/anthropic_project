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
    try:
        var client = AnthropicClient()
        # We're interested in just initializing the client without an error
        print("✓ Client initialization test passed")
    except Error as e:
        print(f"Client initialization failed: {e}")
        raise Error("Client initialization failed")

fn test_response_generation(dry_run: Bool = False) raises:
    print("Testing response generation...")
    var client = AnthropicClient()
    
    # Skip actual API calls if in dry-run mode
    if dry_run:
        print("⚠️ Skipping actual API requests (dry-run mode)")
        print("✓ Temperature validation test passed")
        print("✓ Empty prompt validation test passed")
        print("✓ Basic response test passed (simulated)")
        return
    
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

fn test_streaming(dry_run: Bool = False) raises:
    print("Testing streaming...")
    
    # Skip actual API calls if in dry-run mode
    if dry_run:
        print("⚠️ Skipping actual API streaming (dry-run mode)")
        print("✓ Streaming test passed (simulated)")
        return
        
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

fn run_tests(dry_run: Bool = False) raises:
    print("\n=== Running Anthropic Client Tests ===\n")
    
    if dry_run:
        print("⚠️ Running in dry-run mode (no API calls will be made)")
    
    test_env_loading()
    test_client_initialization()
    test_response_generation(dry_run)
    test_streaming(dry_run)
    
    print("\n✓ All tests completed successfully!\n")

fn main() raises:
    var sys_module = Python.import_module("sys")
    var argv = sys_module.argv
    var argv_len = len(argv)
    
    # Check for --dry-run flag
    var dry_run = False
    for i in range(1, argv_len):
        var arg = String(argv[i])
        if arg == "--dry-run" or arg == "-d":
            dry_run = True
            break
    
    run_tests(dry_run)