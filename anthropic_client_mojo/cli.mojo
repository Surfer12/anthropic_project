"""
Command line interface for the Anthropic Claude API client.
Mojo version of the original Python CLI.
"""

import sys
import time
from python import Python
from python import PythonObject

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
        type=Python.float,
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
    if len(args.prompt) > 0:
        var join_fn = Python.evaluate(" ' '.join")
        prompt = String(join_fn(args.prompt))
    else:
        var stderr = sys_module.stderr
        stderr.write("Enter your prompt (Ctrl+D to submit):\n")
        stderr.flush()
        
        var stdin_read = sys_module.stdin.read()
        prompt = String(stdin_read.strip())
        
        if len(prompt) == 0:
            stderr.write("Error: No prompt provided\n")
            sys_module.exit(1)
    
    try:
        var client = AnthropicClient()
        var stdout = sys_module.stdout
        
        if args.stream:
            # Stream response with real-time output
            stdout.write("Claude: ")
            stdout.flush()
            
            var response_iterator = client.get_response(prompt, True, Float64(args.temperature))
            
            var time_module = Python.import_module("time")
            
            for chunk in response_iterator:
                var chunk_text = String(chunk)
                stdout.write(chunk_text)
                stdout.flush()
                time_module.sleep(0.01)  # Small delay for smoother output
            
            stdout.write("\n")  # Final newline
        else:
            # Get complete response
            var response = client.get_response(prompt, False, Float64(args.temperature))
            stdout.write("Claude: " + String(response) + "\n")
    
    except Error as e:
        var stderr = sys_module.stderr
        stderr.write("Error: " + e + "\n")
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