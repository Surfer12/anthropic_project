import os
import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anthropic_client import AnthropicClient
from dotenv import load_dotenv


class TestAnthropicClient:
    """Test suite for the Anthropic client module."""

    def test_module_imports(self):
        """Test that necessary modules can be imported."""
        assert 'anthropic' in sys.modules
        assert 'os' in sys.modules
        assert 'dotenv' in sys.modules

    @patch('anthropic.Anthropic')
    def test_client_initialization(self, mock_anthropic):
        """Test client initialization with API key."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            assert client.client == mock_anthropic.return_value

    @patch('anthropic.Anthropic')
    def test_missing_api_key(self, mock_anthropic):
        """Test handling of missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable not set"):
                AnthropicClient()

    @patch('anthropic.Anthropic')
    def test_get_response_non_streaming(self, mock_anthropic):
        """Test non-streaming response."""
        # Setup mock client and response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Hello, human!"}]
        mock_client.beta.messages.create.return_value = mock_message

        # Create client and get response
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            result = client.get_response("Test prompt")

        # Verify API called with correct parameters
        mock_client.beta.messages.create.assert_called_once()
        args = mock_client.beta.messages.create.call_args[1]
        assert args["model"] == "claude-3-7-sonnet-20250219"
        assert args["max_tokens"] == 128000
        assert args["temperature"] == 1.0
        assert args["messages"][0]["role"] == "user"
        assert args["messages"][0]["content"] == "Test prompt"
        assert args["thinking"]["type"] == "enabled"
        assert args["thinking"]["budget_tokens"] == 128000
        assert "output-128k-2025-02-19" in args["betas"]
        assert not args.get("stream", False)
        
        # Verify result
        assert result == "Hello, human!"

    @patch('anthropic.Anthropic')
    def test_get_response_with_temperature(self, mock_anthropic):
        """Test response with custom temperature."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Hello, human!"}]
        mock_client.beta.messages.create.return_value = mock_message

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            result = client.get_response("Test prompt", temperature=0.5)

        args = mock_client.beta.messages.create.call_args[1]
        assert args["temperature"] == 0.5
        assert result == "Hello, human!"

    @patch('anthropic.Anthropic')
    def test_get_response_streaming(self, mock_anthropic):
        """Test streaming response."""
        # Setup mock client and streaming response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_chunks = [
            MagicMock(content=[MagicMock(text="Hello")]),
            MagicMock(content=[MagicMock(text=", ")]),
            MagicMock(content=[MagicMock(text="human!")])
        ]
        mock_client.beta.messages.create.return_value = mock_chunks

        # Create client and get streaming response
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            result = client.get_response("Test prompt", stream=True)

        # Verify streaming was requested
        mock_client.beta.messages.create.assert_called_once()
        assert mock_client.beta.messages.create.call_args[1]["stream"] == True

        # Collect streaming response
        response_chunks = list(result)
        assert response_chunks == ["Hello", ", ", "human!"]