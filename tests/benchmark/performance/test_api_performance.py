"""Performance benchmarks for API operations."""

import os
import pytest
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_client():
    """Create an Anthropic client."""
    return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "dummy_key_for_testing"))

@pytest.fixture
def client():
    """Create an Anthropic client for testing."""
    return create_client()

def test_client_initialization(benchmark):
    """Benchmark client initialization time."""
    benchmark(create_client)

def test_message_completion(benchmark, client):
    """Benchmark message completion time."""
    # Skip this test if no API key is provided
    if os.environ.get("ANTHROPIC_API_KEY") is None:
        pytest.skip("No API key provided, skipping test_message_completion")
        
    def run_completion():
        return client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Hello, how are you?"
            }]
        )
    
    result = benchmark(run_completion)
    assert result is not None
    assert len(result.content) > 0 