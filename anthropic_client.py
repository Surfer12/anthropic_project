import os
import anthropic
from dotenv import load_dotenv

def get_response():
    # Load API key from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = anthropic.Anthropic(
        api_key=api_key
    )

    message = client.beta.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=128000,
        temperature=1,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ],
        thinking={
            "type": "enabled",
            "budget_tokens": 64000
        },
        betas=["output-128k-2025-02-19"]
    )
    return message.content

if __name__ == "__main__":
    try:
        response = get_response()
        print(response)
    except Exception as e:
        print(f"Error: {e}")