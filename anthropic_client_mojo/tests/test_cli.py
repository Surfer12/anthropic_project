import pytest
from unittest.mock import patch, MagicMock
import sys
import io
import os
import anthropic
from anthropic_client_mojo.python_cli import create_parser, run_cli, main

def test_parser_creation():
    """Test that argument parser is created correctly."""
    parser = create_parser()
    
    # Test with command line arguments
    args = parser.parse_args(["Hello", "Claude"])
    assert args.prompt == ["Hello", "Claude"]
    assert not args.stream
    assert args.temperature == 1.0

    # Test with stream option
    args = parser.parse_args(["-s", "Hello"])
    assert args.stream
    assert args.prompt == ["Hello"]

    # Test with temperature
    args = parser.parse_args(["-t", "0.5", "Hello"])
    assert args.temperature == 0.5
    assert args.prompt == ["Hello"]

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_args():
    """Test main function with command line arguments."""
    # Setup mock
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.return_value = [
            MagicMock(delta=MagicMock(text="Test response"))
        ]

        # Test with arguments
        test_args = ["cli.py", "Test", "prompt"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                main()
                assert "Test response" in fake_out.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_stream():
    """Test main function with streaming enabled."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.return_value = [
            MagicMock(delta=MagicMock(text="Hello")),
            MagicMock(delta=MagicMock(text=", ")),
            MagicMock(delta=MagicMock(text="World"))
        ]

        # Test with streaming
        test_args = ["cli.py", "-s", "Test", "prompt"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                with patch('time.sleep'):  # Skip sleep delays
                    main()
                assert "Hello, World" in fake_out.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_error():
    """Test main function error handling."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = ValueError("Test error")

        # Test error handling
        test_args = ["cli.py", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error: Test error" in fake_err.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_invalid_temperature():
    """Test main function with invalid temperature value."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        test_args = ["cli.py", "-t", "2.0", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error: Temperature must be between 0.0 and 1.0" in fake_err.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_keyboard_interrupt():
    """Test main function handling of keyboard interrupt."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = KeyboardInterrupt()

        test_args = ["cli.py", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Operation cancelled by user" in fake_err.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_streaming_keyboard_interrupt():
    """Test main function handling of keyboard interrupt during streaming."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        def mock_stream():
            yield MagicMock(delta=MagicMock(text="Hello"))
            raise KeyboardInterrupt()

        mock_client.beta.messages.create.return_value = mock_stream()

        test_args = ["cli.py", "-s", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 1
                    assert "Operation cancelled by user" in fake_err.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_rate_limit_error():
    """Test main function handling of rate limit errors."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = anthropic.RateLimitError(
            message="Rate limit exceeded",
            request=MagicMock(),
            response=MagicMock(status_code=429),
            body={"error": {"message": "Rate limit exceeded"}}
        )

        test_args = ["cli.py", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error: Rate limit exceeded" in fake_err.getvalue()

@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
def test_main_with_unexpected_error():
    """Test main function handling of unexpected errors."""
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.beta.messages.create.side_effect = Exception("Unexpected error")

        test_args = ["cli.py", "Test"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stderr', new=io.StringIO()) as fake_err:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "An unexpected error occurred: Unexpected error" in fake_err.getvalue()

def test_parser_invalid_temperature():
    """Test argument parser with invalid temperature values."""
    parser = create_parser()
    
    # Test non-numeric temperature
    with pytest.raises(SystemExit):
        parser.parse_args(["-t", "invalid", "Test"])
    
    # Test missing temperature value
    with pytest.raises(SystemExit):
        parser.parse_args(["-t"])

@patch('anthropic_client.AnthropicClient')
def test_main_with_rate_limit_error(mock_client_class):
    """Test main function handling of rate limit errors."""
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.get_response.side_effect = ValueError("Rate limit exceeded")
    
    test_args = ["cli.py", "Test"]
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stderr', new=io.StringIO()) as fake_err:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            assert "Error: Rate limit exceeded" in fake_err.getvalue()

@patch('anthropic_client.AnthropicClient')
def test_main_with_unexpected_error(mock_client_class):
    """Test main function handling of unexpected errors."""
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.get_response.side_effect = Exception("Unexpected error")
    
    test_args = ["cli.py", "Test"]
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stderr', new=io.StringIO()) as fake_err:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            assert "An unexpected error occurred: Unexpected error" in fake_err.getvalue() 