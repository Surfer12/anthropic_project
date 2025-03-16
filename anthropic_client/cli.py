"""
Command line interface for the Anthropic Claude API client.
"""

import argparse
import sys
import time
import json
import os
from pathlib import Path
from typing import Optional, Iterator, NoReturn, TextIO
import logging
from .client import AnthropicClient, ModelName, OutputFormat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
STREAM_DELAY: float = 0.01  # Delay between chunks when streaming
DEFAULT_TEMPERATURE: float = 1.0
DEFAULT_MODEL: ModelName = ModelName.SONNET
DEFAULT_FORMAT: OutputFormat = OutputFormat.TEXT

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for the CLI.
    
    Returns:
        An ArgumentParser instance configured with all CLI options.
    """
    parser = argparse.ArgumentParser(
        description="Command line interface for the Anthropic Claude API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="The prompt to send to Claude. If not provided, reads from stdin."
    )
    parser.add_argument(
        "-ns", "--no-stream",
        action="store_true",
        help="Disable streaming (get complete response at once)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Temperature for response generation ({AnthropicClient.MIN_TEMPERATURE} to {AnthropicClient.MAX_TEMPERATURE})"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default=DEFAULT_MODEL.value,
        choices=[model.value for model in ModelName],
        help="Model to use for response generation"
    )
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=[fmt.value for fmt in OutputFormat],
        default=DEFAULT_FORMAT.value,
        help="Format for the response output"
    )
    parser.add_argument(
        "--system",
        type=str,
        help="System prompt to set context/permissions"
    )
    parser.add_argument(
        "--haiku",
        action="store_true",
        help="Generate a 3-5-3 haiku in response to the prompt"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Enable interactive mode for back-and-forth dialogue"
    )
    parser.add_argument(
        "--save-conversation",
        type=str,
        metavar="FILENAME",
        help="Save the conversation to a JSON file"
    )
    parser.add_argument(
        "--load-conversation",
        type=str,
        metavar="FILENAME",
        help="Load a conversation from a JSON file"
    )
    parser.add_argument(
        "--model-config",
        type=str,
        help="Path to a JSON file containing model configuration"
    )
    return parser

def get_prompt_from_stdin() -> str:
    """Read prompt from standard input.
    
    Returns:
        The prompt string read from stdin.
        
    Raises:
        argparse.ArgumentError: If no prompt is provided.
    """
    print("Enter your prompt (Ctrl+D to submit):", file=sys.stderr)
    prompt = sys.stdin.read().strip()
    if not prompt:
        raise argparse.ArgumentError(None, "No prompt provided")
    return prompt

def handle_streaming_response(
    client: AnthropicClient,
    prompt: str,
    temperature: float,
    model: str,
    format: str,
    system: Optional[str]
) -> None:
    """Handle streaming response from Claude.
    
    Args:
        client: The AnthropicClient instance
        prompt: The user's prompt
        temperature: Response temperature
        model: Model name
        format: Output format
        system: Optional system prompt
    """
    print("Claude: ", end="", flush=True)
    try:
        for chunk in client.get_response(
            prompt,
            stream=True,
            temperature=temperature,
            model=model,
            format=format,
            system=system
        ):
            print(chunk, end="", flush=True)
            time.sleep(STREAM_DELAY)
        print()  # Final newline
    except KeyboardInterrupt:
        print("\nStreaming cancelled by user", file=sys.stderr)
        raise

def handle_complete_response(
    client: AnthropicClient,
    prompt: str,
    temperature: float,
    model: str,
    format: str,
    system: Optional[str]
) -> None:
    """Handle complete (non-streaming) response from Claude.
    
    Args:
        client: The AnthropicClient instance
        prompt: The user's prompt
        temperature: Response temperature
        model: Model name
        format: Output format
        system: Optional system prompt
    """
    response = client.get_response(
        prompt,
        stream=False,
        temperature=temperature,
        model=model,
        format=format,
        system=system
    )
    print("Claude:", response)

def main() -> NoReturn:
    """Main entry point for the CLI application."""
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        # Check for CLI invocation name for model presets
        program_name = sys.argv[0].lower()
        if "haiku" in program_name and args.model == ModelName.SONNET.value:
            args.model = ModelName.HAIKU.value

        # Get prompt from arguments or stdin
        prompt = " ".join(args.prompt) if args.prompt else get_prompt_from_stdin()

        model_config = None
        if args.model_config:
            with open(args.model_config, 'r') as f:
                model_config = json.load(f)

        # Example: instantiating MultiProviderClient
        from anthropic_client.multi_provider_client import MultiProviderClient
        client = MultiProviderClient()
        
        if args.no_stream:
            handle_complete_response(
                client,
                prompt,
                args.temperature,
                args.model,
                args.format,
                args.system
            )
        else:
            handle_streaming_response(
                client,
                prompt,
                args.temperature,
                args.model,
                args.format,
                args.system
            )
            
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 