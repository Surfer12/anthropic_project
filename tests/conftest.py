import os
import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_env_setup():
    """Set up test environment variables."""
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-api-key-for-testing"}):
        yield


@pytest.fixture
def mock_anthropic_response():
    """Return a mock Anthropic API response."""
    return {"type": "text", "text": "Hello, this is a test response from Claude."}