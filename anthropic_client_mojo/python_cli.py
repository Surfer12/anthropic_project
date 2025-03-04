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
    
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Test mode that doesn't make actual API calls"
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
        
        # Dry run mode for testing without API calls
        if args.dry_run:
            sys.stdout.write("=== DRY RUN MODE ===\n")
            sys.stdout.write(f"API Key found: {'Yes' if api_key else 'No'}\n")
            sys.stdout.write(f"Prompt: {prompt}\n")
            sys.stdout.write(f"Stream mode: {args.stream}\n")
            sys.stdout.write(f"Temperature: {args.temperature}\n")
            sys.stdout.write("Claude: [This is a dry run test response.]\n")
            return
            
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