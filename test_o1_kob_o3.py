#!/usr/bin/env python3
"""
Test script for the o1-kob-o3 model integration.
"""

from anthropic_client.multi_provider_client import MultiProviderClient
from anthropic_client.client import ModelName

def main():
    """Test the o1-kob-o3 model integration."""
    client = MultiProviderClient()
    
    prompt = "Explain the concept of recursive knowledge mapping in 3 sentences."
    
    try:
        # Test using the enum
        response = client.get_response(
            prompt=prompt,
            model=ModelName.O1_KOB_O3,
            temperature=0.7
        )
        print("Response using enum:")
        print(response)
        print("\n" + "-" * 50 + "\n")
        
        # Test using the string
        response = client.get_response(
            prompt=prompt,
            model="o1-kob-o3",
            temperature=0.7
        )
        print("Response using string:")
        print(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 