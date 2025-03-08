import os
import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anthropic_client import AnthropicClient
from dotenv import load_dotenv
import anthropic


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
    def test_get_response_empty_prompt(self, mock_anthropic):
        """Test handling of empty prompts."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            
            # Test empty string
            with pytest.raises(ValueError, match="Prompt cannot be empty"):
                client.get_response("")
                
            # Test whitespace only
            with pytest.raises(ValueError, match="Prompt cannot be empty"):
                client.get_response("   ")

    @patch('anthropic.Anthropic')
    def test_get_response_api_error(self, mock_anthropic):
        """Test handling of API errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Simulate API error
        mock_client.beta.messages.create.side_effect = anthropic.APIError("API Error")
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            with pytest.raises(anthropic.APIError, match="API Error"):
                client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_get_response_rate_limit(self, mock_anthropic):
        """Test handling of rate limit errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Simulate rate limit error
        mock_client.beta.messages.create.side_effect = anthropic.RateLimitError("Rate limit exceeded")
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            with pytest.raises(anthropic.RateLimitError, match="Rate limit exceeded"):
                client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_get_response_invalid_api_key(self, mock_anthropic):
        """Test handling of invalid API key."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Simulate authentication error
        mock_client.beta.messages.create.side_effect = anthropic.AuthenticationError("Invalid API key")
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "invalid-key"}):
            client = AnthropicClient()
            with pytest.raises(anthropic.AuthenticationError, match="Invalid API key"):
                client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_get_response_streaming_error(self, mock_anthropic):
        """Test handling of streaming errors."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Simulate streaming error
        def mock_stream():
            yield MagicMock(content=[MagicMock(text="Hello")])
            raise anthropic.APIError("Stream error")
            
        mock_client.beta.messages.create.return_value = mock_stream()
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            response = client.get_response("Test prompt", stream=True)
            
            # First chunk should work
            assert next(response) == "Hello"
            
            # Second chunk should raise error
            with pytest.raises(anthropic.APIError, match="Stream error"):
                next(response)

    @patch('anthropic.Anthropic')
    def test_logging_configuration(self, mock_anthropic):
        """Test that logging is properly configured."""
        import logging
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            # Test with debug logging
            logging.basicConfig(level=logging.DEBUG)
            client = AnthropicClient()
            
            mock_message = MagicMock()
            mock_message.content = [{"type": "text", "text": "Test response"}]
            mock_anthropic.return_value.beta.messages.create.return_value = mock_message
            
            with self.assertLogs(level='DEBUG') as log:
                client.get_response("Test prompt")
                assert any("Sending request to Anthropic API" in msg for msg in log.output)
                assert any("Received response from Anthropic API" in msg for msg in log.output)

    @patch('anthropic.Anthropic')
    def test_timeout_handling(self, mock_anthropic):
        """Test handling of timeout errors."""
        from requests.exceptions import Timeout
        
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = Timeout("Request timed out")
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            with pytest.raises(Timeout, match="Request timed out"):
                client.get_response("Test prompt")

    @patch('anthropic.Anthropic')
    def test_thinking_budget_validation(self, mock_anthropic):
        """Test validation of thinking budget parameter."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            
            # Test invalid thinking budget
            with pytest.raises(ValueError, match="Thinking budget must be between 1 and 128000"):
                client.get_response("Test prompt", thinking_budget=0)
            
            with pytest.raises(ValueError, match="Thinking budget must be between 1 and 128000"):
                client.get_response("Test prompt", thinking_budget=128001)

    @patch('anthropic.Anthropic')
    def test_response_content_types(self, mock_anthropic):
        """Test handling of different response content types."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Test text content
        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Text response"}]
        mock_client.beta.messages.create.return_value = mock_message
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            client = AnthropicClient()
            result = client.get_response("Test prompt")
            assert result == "Text response"
        
        # Test empty content
        mock_message.content = []
        result = client.get_response("Test prompt")
        assert result == ""
        
        # Test multiple content blocks
        mock_message.content = [
            {"type": "text", "text": "First"},
            {"type": "text", "text": " Second"}
        ]
        result = client.get_response("Test prompt")
        assert result == "First Second"

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