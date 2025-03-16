from anthropic_client import AnthropicClient

# Extract a prompt structure from the example
def get_example_prompt():
    import json
    with open('anthropic_client/o1-kob.py') as f:
        data = json.load(f)
    return data['input'][0]['content'][0]['text']

# Use as a starting point for a new prompt
client = AnthropicClient()
example = get_example_prompt()
custom_prompt = example.replace("recursive model", "my custom model")
response = client.get_response(custom_prompt)
