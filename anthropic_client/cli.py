"""
Command line interface for the Anthropic Claude API client.
"""

import argparse
import sys
import time
import json
import os
from pathlib import Path
from .client import AnthropicClient

def create_parser() -> argparse.ArgumentParser:
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
        default=1.0,
        help="Temperature for response generation (0.0 to 1.0)"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="claude-3-7-sonnet-20250219",
        choices=["claude-3-7-sonnet-20250219", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
        help="Model to use for response generation"
    )
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["text", "json", "markdown"],
        default="text",
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
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # Check for CLI invocation name for model presets
    program_name = sys.argv[0].lower()
    if "haiku" in program_name and args.model == "claude-3-7-sonnet-20250219":
        args.model = "claude-3-5-haiku-20241022"

    # Get prompt from arguments or stdin
    if args.prompt:
        prompt = " ".join(args.prompt)
    else:
        print("Enter your prompt (Ctrl+D to submit):", file=sys.stderr)
        prompt = sys.stdin.read().strip()
        if not prompt:
            parser.error("No prompt provided")

    try:
        client = AnthropicClient()
        
        if args.no_stream:
            # Get complete response at once
            response = client.get_response(
                prompt,
                stream=False,
                temperature=args.temperature,
                model=args.model,
                format=args.format,
                system=args.system
            )
            print("Claude:", response)
        else:
            # Stream response with real-time output (default)
            print("Claude: ", end="", flush=True)
            for chunk in client.get_response(
                prompt, 
                stream=True,
                temperature=args.temperature,
                model=args.model,
                format=args.format,
                system=args.system
            ):
                print(chunk, end="", flush=True)
                time.sleep(0.01)  # Small delay for smoother output
            print()  # Final newline
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 