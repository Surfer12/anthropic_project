import os
import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic_client
from dotenv import load_dotenv


class TestAnthropicClient:
    """Test suite for the Anthropic client module."""

    def test_module_imports(self):
        """Test that necessary modules can be imported."""
        assert 'anthropic' in sys.modules
        assert 'os' in sys.modules
        assert 'dotenv' in sys.modules

    @patch('anthropic.Anthropic')
    @patch('anthropic_client.load_dotenv')
    def test_get_response_calls_api(self, mock_load_dotenv, mock_anthropic):
        """Test that get_response calls the API with correct parameters."""
        # Setup mock client and response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Hello, human!"}]
        mock_client.beta.messages.create.return_value = mock_message

        # Call the function
        result = anthropic_client.get_response()

        # Verify dotenv was loaded
        mock_load_dotenv.assert_called_once()

        # Verify API called with correct parameters
        mock_client.beta.messages.create.assert_called_once()
        args = mock_client.beta.messages.create.call_args[1]
        assert args["model"] == "claude-3-7-sonnet-20250219"
        assert args["max_tokens"] == 128000
        assert args["temperature"] == 1
        assert args["messages"][0]["role"] == "user"
        assert args["messages"][0]["content"] == "Hello, Claude!"
        assert args["thinking"]["type"] == "enabled"
        assert args["thinking"]["budget_tokens"] == 64000
        assert "output-128k-2025-02-19" in args["betas"]
        
        # Verify result
        assert result == [{"type": "text", "text": "Hello, human!"}]

    @patch('anthropic.Anthropic')
    @patch('anthropic_client.load_dotenv')
    def test_get_response_handling(self, mock_load_dotenv, mock_anthropic):
        """Test that get_response correctly handles the API response."""
        # Setup mock client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Setup mock response with multiple content blocks
        mock_message = MagicMock()
        mock_message.content = [
            {"type": "text", "text": "Part 1"}, 
            {"type": "text", "text": "Part 2"}
        ]
        mock_client.beta.messages.create.return_value = mock_message
        
        # Call function
        result = anthropic_client.get_response()
        
        # Verify dotenv was loaded
        mock_load_dotenv.assert_called_once()
        
        # Verify proper handling
        assert result == [{"type": "text", "text": "Part 1"}, {"type": "text", "text": "Part 2"}]

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}, clear=True)
    @patch('anthropic.Anthropic')
    @patch('anthropic_client.load_dotenv')
    def test_missing_api_key(self, mock_load_dotenv, mock_anthropic):
        """Test handling of missing API key."""
        # The implementation should raise an exception if no API key is present
        
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable not set"):
            anthropic_client.get_response()