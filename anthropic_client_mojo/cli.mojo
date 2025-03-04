"""
Command line interface for the Anthropic Claude API client.
Mojo version of the original Python CLI.
"""

import sys
import time
from python import Python, PythonObject

from client import AnthropicClient

fn create_parser() raises -> PythonObject:
    """Create and configure the argument parser."""
    var argparse = Python.import_module("argparse")
    var parser = argparse.ArgumentParser(
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
        type=Python.evaluate("float"),
        default=1.0,
        help="Temperature for response generation (0.0 to 1.0)"
    )
    
    return parser

fn main() raises:
    """Main entry point for the CLI application."""
    var parser = create_parser()
    var sys_module = Python.import_module("sys")
    var args = parser.parse_args()
    
    var prompt: String = ""
    
    # Get prompt from arguments or stdin
    var py_args = Python.evaluate("""
    def get_prompt_from_args(args):
        if args.prompt and len(args.prompt) > 0:
            return ' '.join(args.prompt)
        else:
            import sys
            sys.stderr.write("Enter your prompt (Ctrl+D to submit):\\n")
            sys.stderr.flush()
            try:
                stdin_read = sys.stdin.read()
                prompt = stdin_read.strip()
                if not prompt:
                    sys.stderr.write("Error: No prompt provided\\n")
                    sys.exit(1)
                return prompt
            except KeyboardInterrupt:
                sys.stderr.write("\\nOperation cancelled by user\\n")
                sys.exit(1)
            except:
                sys.stderr.write("Error: Failed to read input\\n")
                sys.exit(1)
    
    get_prompt_from_args
    """)
    
    prompt = String(py_args(args))
    
    # Create a wrapper for the client interaction
    var runner = Python.evaluate("""
    def run_client(prompt_text, stream_mode, temperature_value):
        import sys
        import time
        import anthropic
        
        try:
            # Set up API key from environment
            from dotenv import load_dotenv
            import os
            load_dotenv()
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                sys.stderr.write("Error: ANTHROPIC_API_KEY environment variable not set\\n")
                return False
                
            # Create Anthropic client directly
            client = anthropic.Anthropic(api_key=api_key)
            
            # Parameters common to both streaming and non-streaming
            params = {
                "model": "claude-3-7-sonnet-20250219",
                "max_tokens": 128000,
                "messages": [{"role": "user", "content": prompt_text}],
                "temperature": float(temperature_value),
                "thinking": {"type": "enabled", "budget_tokens": 120000},
                "betas": ["output-128k-2025-02-19"]
            }
            
            if stream_mode:
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
                
                sys.stdout.write("\\n")  # Final newline
                return True
            else:
                response = client.beta.messages.create(**params)
                response_text = response.content[0].text if response and response.content else "No response"
                sys.stdout.write("Claude: " + response_text + "\\n")
                return True
                
        except Exception as e:
            sys.stderr.write(f"Error: {e}\\n")
            return False
    
    run_client
    """)
    
    try:
        var success = runner(prompt, args.stream, args.temperature)
        
        if not success:
            sys_module.exit(1)
    
    except:
        var stderr = sys_module.stderr
        stderr.write("Error: An unexpected error occurred\n")
        sys_module.exit(1)

fn run_main() raises:
    """Entry point with exception handling for keyboard interrupts."""
    try:
        main()
    except:
        var sys_module = Python.import_module("sys")
        var stderr = sys_module.stderr
        stderr.write("\nOperation cancelled by user\n")
        sys_module.exit(1)