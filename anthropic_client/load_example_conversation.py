import json

def load_example_conversation():
    with open('anthropic_client/o1-kob.py') as f:
        data = json.load(f)
    return data

# Access model type
model_info = load_example_conversation()
print(f"Using model: {model_info['model']}")

# Access the prompts or responses
for interaction in model_info['input']:
    if interaction['role'] == 'developer':
        print("Developer prompt:", interaction['content'][0]['text'][:100], "...")