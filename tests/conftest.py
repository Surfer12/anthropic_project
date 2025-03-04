import os
import pytest
from unittest.mock import patch, MagicMock
import io
import anthropic


@pytest.fixture(autouse=True)
def mock_env_setup():
    """Set up test environment variables."""
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key-for-testing"}):
        yield


@pytest.fixture
def mock_anthropic_response():
    """Return a mock Anthropic API response."""
    return {"type": "text", "text": "Hello, this is a test response from Claude."}


@pytest.fixture
def mock_anthropic_client():
    """Return a mock Anthropic client."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Setup default response
        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Test response"}]
        mock_client.beta.messages.create.return_value = mock_message
        
        yield mock_client


@pytest.fixture
def mock_streaming_response():
    """Return a mock streaming response."""
    return [
        MagicMock(content=[MagicMock(text="First")]),
        MagicMock(content=[MagicMock(text=" chunk")]),
        MagicMock(content=[MagicMock(text=" response")])
    ]


@pytest.fixture
def mock_cli_args():
    """Return mock CLI arguments."""
    return {
        'basic': ["cli.py", "Test prompt"],
        'with_temperature': ["cli.py", "-t", "0.7", "Test prompt"],
        'with_stream': ["cli.py", "-s", "Test prompt"],
        'empty': ["cli.py"],
    }


@pytest.fixture
def captured_output():
    """Capture stdout and stderr."""
    class CapturedOutput:
        def __init__(self):
            self.stdout = io.StringIO()
            self.stderr = io.StringIO()
    
    return CapturedOutput()


@pytest.fixture
def anthropic_error_responses():
    """Return common Anthropic API error responses."""
    return {
        'api_error': anthropic.APIError("API Error"),
        'rate_limit': anthropic.RateLimitError("Rate limit exceeded"),
        'auth_error': anthropic.AuthenticationError("Invalid API key"),
        'invalid_request': anthropic.InvalidRequestError("Invalid request"),
    }