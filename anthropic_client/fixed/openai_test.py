from openai import OpenAI
import os
import json
import sys

# Get API key from environment variable or set it directly
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    print("Example: export OPENAI_API_KEY='your-api-key'")
    sys.exit(1)

print("Initializing OpenAI client...")
try:
    # Configure the client with standard settings
    client = OpenAI(api_key=api_key)
    
    print("Testing connectivity to OpenAI API...")
    # Simple API test to verify connection works
    models = client.models.list()
    print(f"Connection successful! Available models: {len(models.data)}")
    
    print("\nSending request to GPT-4o...")
    response = client.chat.completions.create(
        model="gpt-4o",  # Using GPT-4o instead of gpt-4.5-preview
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides responses in JSON format."
            },
            {
                "role": "user", 
                "content": "Create a JSON representation of a cognitive framework with multi-level insight generation capabilities."
            }
        ],
        response_format={"type": "json_object"}
    )
    
    print("\nResponse received:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 