import os
import anthropic
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_response():
    client = anthropic.Anthropic(
        # Use environment variable for API key
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    with client.beta.messages.stream(
        model="claude-3-7-sonnet-20250219",
        max_tokens=128000,  # Maximum allowed for claude-3-7-sonnet-20250219
        temperature=1,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ],
        thinking={
            "type": "enabled",
            "budget_tokens": 64000  # Reduced to be less than max_tokens
        },
        betas=["output-128k-2025-02-19"]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print()  # Final newline after completion
        return stream.get_final_message().content

if __name__ == "__main__":
    get_response()