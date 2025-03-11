"""
Main entry point for the Mojo version of the Anthropic Claude API client.
Provides CLI guidance and project information.
"""

from python import Python

fn main() raises:
    print("🤖 Anthropic Claude Mojo Client CLI 🤖")
    print("\n--- Project Overview ---")
    print("A high-performance Mojo implementation of the Anthropic Claude API client")
    print("Optimized for: Performance, Caching, Parallel Processing\n")
    
    print("--- CLI Usage Options ---")
    var show_help = Python.evaluate("""
    lambda: print('''
    Usage Modes:
    1. Standard Interaction:
       python python_cli.py 'Your prompt here'

    2. Streaming Response:
       python python_cli.py -s 'Your prompt here'

    3. Dry Run (Test Mode):
       python python_cli.py -d 'Your prompt here'

    Options:
      -h, --help         Show this help message
      -s, --stream       Stream the response
      -t, --temperature  Set response temperature (0.0-1.0)
      -d, --dry-run      Test mode without API calls
    ''')
    """)
    show_help()
    
    print("\n--- Quick Start ---")
    print("1. Ensure Mojo and Python are installed")
    print("2. Set up Anthropic API credentials")
    print("3. Run the CLI with your desired prompt\n")
    
    print("For more details, check the documentation in docs/README.md")