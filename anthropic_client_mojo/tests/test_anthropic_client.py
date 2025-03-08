import os
import sys
import pytest
import unittest
import anthropic
from unittest.mock import patch, MagicMock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anthropic_client import AnthropicClient
from dotenv import load_dotenv


class TestAnthropicClient(unittest.TestCase):
    """Test suite for the Anthropic client module."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = "test-key"
        self.mock_env = patch.dict(os.environ, {"ANTHROPIC_API_KEY": self.api_key})
        self.mock_env.start()

    def tearDown(self):
        """Clean up test environment."""
        self.mock_env.stop()

    def test_module_imports(self):
        """Test that necessary modules can be imported."""
        assert 'anthropic' in sys.modules
        assert 'os' in sys.modules
        assert 'dotenv' in sys.modules

    @patch('anthropic.Anthropic')
    def test_client_initialization(self, mock_anthropic):
        """Test client initialization."""
        client = AnthropicClient()
        mock_anthropic.assert_called_once_with(api_key=self.api_key)

    @patch('anthropic.Anthropic')
    def test_missing_api_key(self, mock_anthropic):
        """Test handling of missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as cm:
                AnthropicClient()
            self.assertEqual(str(cm.exception), "ANTHROPIC_API_KEY environment variable not set")

    @patch('anthropic.Anthropic')
    def test_get_response_non_streaming(self, mock_anthropic):
        """Test getting a non-streaming response."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Test response"}]
        mock_client.beta.messages.create.return_value = mock_message

        client = AnthropicClient()
        response = client.get_response("Test prompt")
        self.assertEqual(response, "Test response")

    @patch('anthropic.Anthropic')
    def test_get_response_with_temperature(self, mock_anthropic):
        """Test response with custom temperature."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Test response"}]
        mock_client.beta.messages.create.return_value = mock_message

        client = AnthropicClient()
        response = client.get_response("Test prompt", temperature=0.7)
        self.assertEqual(response, "Test response")

        args = mock_client.beta.messages.create.call_args[1]
        self.assertEqual(args["temperature"], 0.7)

    @patch('anthropic.Anthropic')
    def test_get_response_empty_prompt(self, mock_anthropic):
        """Test handling of empty prompt."""
        client = AnthropicClient()
        with self.assertRaises(ValueError) as cm:
            client.get_response("")
        self.assertEqual(str(cm.exception), "Prompt cannot be empty")

    @patch('anthropic.Anthropic')
    def test_get_response_api_error(self, mock_anthropic):
        """Test handling of API errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = anthropic.APIError(
            message="API Error",
            request=MagicMock()
        )

        client = AnthropicClient()
        with self.assertRaises(anthropic.APIError):
            client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_get_response_rate_limit(self, mock_anthropic):
        """Test handling of rate limit errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = anthropic.RateLimitError(
            message="Rate limit exceeded",
            request=MagicMock(),
            response=MagicMock(status_code=429),
            body={"error": {"message": "Rate limit exceeded"}}
        )

        client = AnthropicClient()
        with self.assertRaises(anthropic.RateLimitError):
            client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_get_response_invalid_api_key(self, mock_anthropic):
        """Test handling of invalid API key."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = anthropic.AuthenticationError(
            message="Invalid API key",
            response=MagicMock(status_code=401),
            body={"error": {"message": "Invalid API key"}}
        )

        client = AnthropicClient()
        with self.assertRaises(anthropic.AuthenticationError):
            client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_get_response_streaming_error(self, mock_anthropic):
        """Test handling of streaming errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        def mock_stream():
            yield MagicMock(delta=MagicMock(text="Hello"))
            raise anthropic.APIError(message="Stream error", request=MagicMock())

        mock_client.beta.messages.create.return_value = mock_stream()

        client = AnthropicClient()
        with self.assertRaises(anthropic.APIError):
            client.get_response("Test prompt", stream=True)

    @patch('anthropic.Anthropic')
    def test_logging_configuration(self, mock_anthropic):
        """Test logging configuration."""
        with self.assertLogs(level='INFO') as log:
            client = AnthropicClient()
            client.get_response("Test prompt")
            self.assertTrue(any("Sending request" in msg for msg in log.output))

    @patch('anthropic.Anthropic')
    def test_response_content_types(self, mock_anthropic):
        """Test handling of different response content types."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Test text content
        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Text response"}]
        mock_client.beta.messages.create.return_value = mock_message

        client = AnthropicClient()
        response = client.get_response("Test prompt")
        self.assertEqual(response, "Text response")

        # Test empty content
        mock_message.content = []
        response = client.get_response("Test prompt")
        self.assertEqual(response, "")

        # Test multiple content blocks
        mock_message.content = [
            {"type": "text", "text": "First"},
            {"type": "text", "text": " Second"}
        ]
        response = client.get_response("Test prompt")
        self.assertEqual(response, "First Second")

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
        client = AnthropicClient()
        result = client.get_response("Test prompt", stream=True)

        # Verify streaming was requested
        mock_client.beta.messages.create.assert_called_once()
        assert mock_client.beta.messages.create.call_args[1]["stream"] == True

        # Collect streaming response
        response_chunks = list(result)
        assert response_chunks == ["Hello", ", ", "human!"]

    @patch('anthropic.Anthropic')
    def test_get_response_with_invalid_temperature(self, mock_anthropic):
        """Test response with invalid temperature values."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            
            # Test temperature too high
            with pytest.raises(ValueError, match="Temperature must be between 0.0 and 1.0"):
                client.get_response("Test prompt", temperature=1.5)
                
            # Test temperature too low
            with pytest.raises(ValueError, match="Temperature must be between 0.0 and 1.0"):
                client.get_response("Test prompt", temperature=-0.5)

    @patch('anthropic.Anthropic')
    def test_connection_error_handling(self, mock_anthropic):
        """Test handling of connection errors."""
        from requests.exceptions import ConnectionError
        
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = ConnectionError("Connection failed")
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            with pytest.raises(ConnectionError, match="Connection failed"):
                client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_cleanup_on_error(self, mock_anthropic):
        """Test proper resource cleanup on errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        def mock_stream():
            yield MagicMock(content=[MagicMock(text="Start")])
            raise KeyboardInterrupt()
        
        mock_client.beta.messages.create.return_value = mock_stream()
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            response = client.get_response("Test prompt", stream=True)
            
            # First chunk should work
            assert next(response) == "Start"
            
            # Interrupt should be handled cleanly
            with pytest.raises(KeyboardInterrupt):
                for _ in response:
                    pass