import pytest
from unittest.mock import patch, MagicMock
import sys
import io
from cli import create_parser, main

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

@patch('anthropic_client.AnthropicClient')
def test_main_with_args(mock_client_class):
    """Test main function with command line arguments."""
    # Setup mock
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.get_response.return_value = "Test response"
    
    # Test with command line arguments
    test_args = ["cli.py", "Hello", "Claude"]
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            main()
            assert "Claude: Test response" in fake_out.getvalue()

    # Verify client called correctly
    mock_client.get_response.assert_called_once_with("Hello Claude", stream=False)

@patch('anthropic_client.AnthropicClient')
def test_main_with_stream(mock_client_class):
    """Test main function with streaming enabled."""
    # Setup mock
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.get_response.return_value = ["Hello", ", ", "World"]
    
    # Test with streaming
    test_args = ["cli.py", "-s", "Test", "prompt"]
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            with patch('time.sleep'):  # Skip sleep delays
                main()
                assert "Claude: Hello, World" in fake_out.getvalue()

    # Verify client called correctly
    mock_client.get_response.assert_called_once_with("Test prompt", stream=True)

@patch('anthropic_client.AnthropicClient')
def test_main_with_stdin(mock_client_class):
    """Test main function reading from stdin."""
    # Setup mock
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.get_response.return_value = "Test response"
    
    # Test with stdin input
    test_args = ["cli.py"]
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdin', new=io.StringIO("Test input\n")):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                main()
                assert "Claude: Test response" in fake_out.getvalue()

    # Verify client called correctly
    mock_client.get_response.assert_called_once_with("Test input", stream=False)

@patch('anthropic_client.AnthropicClient')
def test_main_with_error(mock_client_class):
    """Test main function error handling."""
    # Setup mock to raise an error
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.get_response.side_effect = ValueError("Test error")
    
    # Test error handling
    test_args = ["cli.py", "Test"]
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stderr', new=io.StringIO()) as fake_err:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            assert "Error: Test error" in fake_err.getvalue() 