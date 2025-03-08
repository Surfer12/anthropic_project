#!/usr/bin/env python3
"""
Python CLI for Anthropic Claude API.
This is called by the Mojo wrapper.
"""

import sys
import argparse
import time
import json
import anthropic
from typing import Optional, Dict, Any

__version__ = "0.2.0"

AVAILABLE_MODELS = [
    "claude-3-7-sonnet-20250219",
    "claude-3-5-haiku-20241022"
]

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
    
    parser.add_argument(
        "-m", "--model",
        choices=AVAILABLE_MODELS,
        default="claude-3-7-sonnet-20250219",
        help="Claude model to use"
    )
    
    parser.add_argument(
        "-b", "--budget",
        type=int,
        default=120000,
        help="Thinking budget in tokens (1 to 128000)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (text or JSON)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save response to specified file"
    )
    
    parser.add_argument(
        "--system",
        type=str,
        help="System message to set context for Claude"
    )
    
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Test mode that doesn't make actual API calls"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    return parser

def save_response(response: str, output_file: str, format: str = "text") -> None:
    """Save response to a file in specified format."""
    try:
        with open(output_file, 'w') as f:
            if format == "json":
                json.dump({"response": response}, f, indent=2)
            else:
                f.write(response)
    except Exception as e:
        sys.stderr.write(f"Error saving response: {e}\n")

def format_response(response: str, format: str = "text") -> str:
    """Format response in specified format."""
    if format == "json":
        return json.dumps({"response": response}, indent=2)
    return response

def run_cli():
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate temperature when thinking is enabled
    if args.temperature != 1.0 and args.budget > 0:
        sys.stderr.write("Warning: Temperature must be 1.0 when thinking is enabled. Setting temperature to 1.0.\n")
        args.temperature = 1.0
    
    # Get prompt from arguments or stdin
    if args.prompt and len(args.prompt) > 0:
        prompt = ' '.join(args.prompt)
    else:
        sys.stderr.write("Enter your prompt (press Enter twice to submit):\n")
        sys.stderr.flush()
        try:
            lines = []
            while True:
                line = sys.stdin.readline()
                if line.strip() == "" and lines and lines[-1].strip() == "":
                    break
                lines.append(line)
            prompt = ''.join(lines).strip()
            if not prompt:
                sys.stderr.write("Error: No prompt provided\n")
                sys.exit(1)
        except KeyboardInterrupt:
            sys.stderr.write("\nOperation cancelled by user\n")
            sys.exit(1)
        except:
            sys.stderr.write("Error: Failed to read input\n")
            sys.exit(1)
    
    try:
        # Set up API key from environment
        from dotenv import load_dotenv
        import os
        load_dotenv()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        # Dry run mode for testing without API calls
        if args.dry_run:
            sys.stdout.write("=== DRY RUN MODE ===\n")
            sys.stdout.write(f"API Key found: {'Yes' if api_key else 'No'}\n")
            sys.stdout.write(f"Model: {args.model}\n")
            sys.stdout.write(f"Prompt: {prompt}\n")
            sys.stdout.write(f"Stream mode: {args.stream}\n")
            sys.stdout.write(f"Temperature: {args.temperature}\n")
            sys.stdout.write(f"Thinking budget: {args.budget}\n")
            sys.stdout.write(f"Format: {args.format}\n")
            sys.stdout.write(f"Output file: {args.output}\n")
            sys.stdout.write(f"System message: {args.system}\n")
            response = "[This is a dry run test response.]"
            formatted_response = format_response(response, args.format)
            sys.stdout.write(f"Claude: {formatted_response}\n")
            if args.output:
                save_response(response, args.output, args.format)
            return
            
        if not api_key:
            sys.stderr.write("Error: ANTHROPIC_API_KEY environment variable not set\n")
            sys.exit(1)
            
        # Create Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Build messages list
        messages = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        messages.append({"role": "user", "content": prompt})
        
        # Parameters common to both streaming and non-streaming
        params = {
            "model": args.model,
            "max_tokens": 128000,
            "messages": messages,
            "temperature": float(args.temperature),
            "thinking": {"type": "enabled", "budget_tokens": args.budget},
            "stream": True,  # Always use streaming to avoid timeouts
            "betas": ["output-128k-2025-02-19"]
        }
        
        # Add thinking if budget > 0
        if args.budget > 0:
            params["thinking"] = {"type": "enabled", "budget_tokens": args.budget}
        
        # Add system message if provided
        if args.system:
            params["system"] = args.system
        
        # Initialize response accumulator
        full_response = ""
        response_iterator = client.beta.messages.create(**params)
        
        # Handle output based on stream flag
        if args.stream:
            sys.stdout.write("Claude: ")
            sys.stdout.flush()
            
            for chunk in response_iterator:
                chunk_text = str(chunk.delta.text) if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text') else ""
                if chunk_text:
                    full_response += chunk_text
                    sys.stdout.write(chunk_text)
                    sys.stdout.flush()
                    time.sleep(0.01)  # Small delay for smoother output
            
            sys.stdout.write("\n")  # Final newline
        else:
            # Accumulate chunks without displaying
            for chunk in response_iterator:
                chunk_text = str(chunk.delta.text) if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text') else ""
                if chunk_text:
                    full_response += chunk_text
            
            # Format and display complete response
            formatted_response = format_response(full_response, args.format)
            sys.stdout.write(formatted_response + "\n")
        
        # Save response if output file specified
        if args.output:
            save_response(full_response, args.output, args.format)
            
    except anthropic.AuthenticationError as e:
        sys.stderr.write(f"Authentication Error: {e}\n")
        sys.stderr.write("Please check your ANTHROPIC_API_KEY environment variable.\n")
        sys.exit(1)
    except anthropic.APIConnectionError as e:
        sys.stderr.write(f"API Connection Error: {e}\n")
        sys.stderr.write("Please check your internet connection and try again.\n")
        sys.exit(1)
    except anthropic.RateLimitError as e:
        sys.stderr.write(f"Rate Limit Error: {e}\n")
        sys.stderr.write("Please wait a moment and try again.\n")
        sys.exit(1)
    except anthropic.BadRequestError as e:
        sys.stderr.write(f"Bad Request Error: {e}\n")
        sys.exit(1)
    except anthropic.APIError as e:
        sys.stderr.write(f"Anthropic API Error: {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stderr.write("\nOperation cancelled by user\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Unexpected Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()