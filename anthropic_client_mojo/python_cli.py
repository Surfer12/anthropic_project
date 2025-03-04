#!/usr/bin/env python3
"""
Python CLI for Anthropic Claude API.
This is called by the Mojo wrapper.
"""

import sys
import argparse
import time
import anthropic

def run_cli():
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
    
    args = parser.parse_args()
    
    # Get prompt from arguments or stdin
    if args.prompt and len(args.prompt) > 0:
        prompt = ' '.join(args.prompt)
    else:
        sys.stderr.write("Enter your prompt (Ctrl+D to submit):\n")
        sys.stderr.flush()
        try:
            stdin_read = sys.stdin.read()
            prompt = stdin_read.strip()
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
        if not api_key:
            sys.stderr.write("Error: ANTHROPIC_API_KEY environment variable not set\n")
            sys.exit(1)
            
        # Create Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Parameters common to both streaming and non-streaming
        params = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": 128000,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": float(args.temperature),
            "thinking": {"type": "enabled", "budget_tokens": 120000},
            "betas": ["output-128k-2025-02-19"]
        }
        
        if args.stream:
            sys.stdout.write("Claude: ")
            sys.stdout.flush()
            
            # Add streaming parameter
            params["stream"] = True
            response_iterator = client.beta.messages.create(**params)
            
            for chunk in response_iterator:
                chunk_text = str(chunk.delta.text) if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text') else ""
                if chunk_text:
                    sys.stdout.write(chunk_text)
                    sys.stdout.flush()
                    time.sleep(0.01)  # Small delay for smoother output
            
            sys.stdout.write("\n")  # Final newline
        else:
            response = client.beta.messages.create(**params)
            response_text = response.content[0].text if response and response.content else "No response"
            sys.stdout.write("Claude: " + response_text + "\n")
            
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stderr.write("\nOperation cancelled by user\n")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()