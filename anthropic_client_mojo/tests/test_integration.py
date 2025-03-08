import os
import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anthropic_client import AnthropicClient
from anthropic_client_mojo.python_cli import run_cli


class TestIntegration:
    """Integration tests for the Anthropic client and CLI."""

    @patch('anthropic.Anthropic')
    def test_cli_to_client_flow(self, mock_anthropic):
        """Test the complete flow from CLI to client and back."""
        # Setup mock client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        mock_message = MagicMock()
        mock_message.content = [{"type": "text", "text": "Integration test response"}]
        mock_client.beta.messages.create.return_value = mock_message
        
        # Test CLI with custom temperature
        test_args = ["cli.py", "-t", "0.7", "Integration", "test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                main()
        
        # Verify client was called with correct parameters
        args = mock_client.beta.messages.create.call_args[1]
        assert args["temperature"] == 0.7
        assert args["messages"][0]["content"] == "Integration test"
        assert "Integration test response" in fake_out.getvalue()

    @patch('anthropic.Anthropic')
    def test_streaming_integration(self, mock_anthropic):
        """Test streaming integration between CLI and client."""
        # Setup mock client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Setup streaming response
        mock_chunks = [
            MagicMock(content=[MagicMock(text="First")]),
            MagicMock(content=[MagicMock(text=" chunk")]),
            MagicMock(content=[MagicMock(text=" response")])
        ]
        mock_client.beta.messages.create.return_value = mock_chunks
        
        # Test CLI with streaming
        test_args = ["cli.py", "-s", "Stream", "test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with patch('time.sleep'):  # Skip sleep delays
                    main()
        
        # Verify streaming output
        output = fake_out.getvalue()
        assert "Claude: First chunk response" in output

    @patch('anthropic.Anthropic')
    def test_environment_integration(self, mock_anthropic):
        """Test environment variable integration."""
        # Test with missing API key
        with patch.dict(os.environ, {}, clear=True):
            test_args = ["cli.py", "Test"]
            with patch.object(sys, 'argv', test_args):
                with patch('sys.stderr', new=io.StringIO()) as fake_err:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 1
                    assert "ANTHROPIC_API_KEY environment variable not set" in fake_err.getvalue()
        
        # Test with valid API key
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            
            mock_message = MagicMock()
            mock_message.content = [{"type": "text", "text": "Test response"}]
            mock_client.beta.messages.create.return_value = mock_message
            
            test_args = ["cli.py", "Test"]
            with patch.object(sys, 'argv', test_args):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    main()
                assert "Claude: Test response" in fake_out.getvalue()

    @patch('anthropic.Anthropic')
    def test_error_propagation(self, mock_anthropic):
        """Test error propagation from client to CLI."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        # Test API error propagation
        mock_client.beta.messages.create.side_effect = anthropic.APIError("API Error")
        
        test_args = ["cli.py", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error: API Error" in fake_err.getvalue()
        
        # Test rate limit error propagation
        mock_client.beta.messages.create.side_effect = anthropic.RateLimitError("Rate limit")
        
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error: Rate limit" in fake_err.getvalue() 