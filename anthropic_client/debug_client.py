#!/usr/bin/env python3
import sys
import argparse
from anthropic_client.client import AnthropicClient, ModelName, OutputFormat

def main():
    parser = argparse.ArgumentParser(
        description="Debug client for Anthropic's Claude API using AnthropicClient"
    )
    parser.add_argument("prompt", type=str, help="Prompt to send to Claude.")
    parser.add_argument("--stream", action="store_true", help="Stream the response output.")
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Temperature for the response (between 0.0 and 1.0).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=ModelName.SONNET.value,
        help="The Claude model to use (e.g., claude-3-7-sonnet-20250219).",
    )
    parser.add_argument(
        "--format",
        type=str,
        default=OutputFormat.TEXT.value,
        help="Output format: text, json, or markdown.",
    )
    parser.add_argument(
        "--system",
        type=str,
        default=None,
        help="Optional system prompt to set context/permissions.",
    )
    args = parser.parse_args()

    client = AnthropicClient()

    try:
        if args.stream:
            print("Streaming response:")
            for idx, chunk in enumerate(
                client.get_response(
                    prompt=args.prompt,
                    stream=True,
                    temperature=args.temperature,
                    model=args.model,
                    format=args.format,
                    system=args.system,
                )
            ):
                print(f"Chunk {idx+1}: {chunk}")
        else:
            response = client.get_response(
                prompt=args.prompt,
                stream=False,
                temperature=args.temperature,
                model=args.model,
                format=args.format,
                system=args.system,
            )
            print("Response:")
            print(response)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
