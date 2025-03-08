"""Performance benchmarks for API operations."""

import pytest
from anthropic import Anthropic

@pytest.fixture
def client():
    """Create an Anthropic client for testing."""
    return Anthropic()  # Configure as needed

def test_client_initialization(benchmark):
    """Benchmark client initialization time."""
    benchmark(create_client)

def test_message_completion(benchmark, client):
    """Benchmark message completion time."""
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