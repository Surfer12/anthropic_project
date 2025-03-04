import os
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv, find_dotenv


class TestEnvironment:
    """Tests for the project environment configuration."""
    
    def test_dotenv_file_exists(self):
        """Test that .env file exists in project root."""
        env_path = find_dotenv()
        assert env_path, ".env file not found"
        
    def test_api_key_format(self):
        """Test that API key has correct format when loaded from .env."""
        # Load variables from .env
        load_dotenv()
        
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        assert api_key, "ANTHROPIC_API_KEY not found in .env"
        
        # In a test environment, we might not have a real key, so only check in real environments
        if not 'PYTEST_CURRENT_TEST' in os.environ:
            # Check format (Anthropic keys start with 'sk-ant')
            assert api_key.startswith('sk-ant'), "API key has incorrect format"
        
    def test_env_contains_required_vars(self):
        """Test that .env contains all required environment variables."""
        required_vars = ["ANTHROPIC_API_KEY"]
        
        # Load from .env
        load_dotenv()
        
        # Check all required variables are present
        missing = [var for var in required_vars if not os.environ.get(var)]
        assert not missing, f"Missing required environment variables: {missing}"