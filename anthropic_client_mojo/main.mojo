"""
Main entry point for the Mojo version of the Anthropic Claude API client.
"""

from python import Python

fn main() raises:
    print("Running Anthropic Claude CLI (Mojo wrapper)...")
    
    # Create a simple Python function to show CLI usage
    var show_help = Python.evaluate("lambda: print('Anthropic CLI Help\\n\\nUsage: python python_cli.py [prompt]\\n\\nOptions:\\n  -h, --help         Show this help message\\n  -s, --stream       Stream the response\\n  -t, --temperature  Set temperature (0.0-1.0)')")
    show_help()
    
    print("\nTo use the client, please run the Python version directly:")
    print("python anthropic_client_mojo/python_cli.py 'Your prompt here'\n")
    print("For streaming responses:")
    print("python anthropic_client_mojo/python_cli.py -s 'Your prompt here'\n")