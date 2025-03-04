"""
Command line interface for the Anthropic Claude API client.
"""

import argparse
import sys
import time
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
        "-s", "--stream",
        action="store_true",
        help="Stream the response as it's generated"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=1.0,
        help="Temperature for response generation (0.0 to 1.0)"
    )
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

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
        
        if args.stream:
            # Stream response with real-time output
            print("Claude: ", end="", flush=True)
            for chunk in client.get_response(prompt, stream=True):
                print(chunk, end="", flush=True)
                time.sleep(0.01)  # Small delay for smoother output
            print()  # Final newline
        else:
            # Get complete response
            response = client.get_response(prompt)
            print("Claude:", response)
            
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