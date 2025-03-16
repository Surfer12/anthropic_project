import os
import sys
import ssl
import httpx
import certifi
import requests
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

print("=== SSL Certificate Diagnostic Tool ===")

# Check SSL version
print(f"\n1. SSL Version Information:")
print(f"OpenSSL Version: {ssl.OPENSSL_VERSION}")
print(f"Default SSL Context: {ssl.create_default_context()}")

# Check certifi
print(f"\n2. Certificate Information:")
print(f"Certifi version: {certifi.__version__}")
print(f"Certifi path: {certifi.where()}")
print(f"Exists: {os.path.exists(certifi.where())}")

# Test connection to OpenAI with urllib
print(f"\n3. Testing connection to api.openai.com with urllib:")
try:
    with urlopen("https://api.openai.com/v1/models") as response:
        print(f"Success! Status code: {response.status}")
except HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
except URLError as e:
    print(f"URL Error: {e.reason}")
    if isinstance(e.reason, ssl.SSLError):
        print(f"SSL Error details: {e.reason}")
except Exception as e:
    print(f"Error: {e}")

# Test with httpx
print(f"\n4. Testing connection to api.openai.com with httpx:")
try:
    response = httpx.get("https://api.openai.com/v1/models")
    print(f"Success! Status code: {response.status_code}")
except httpx.SSLError as e:
    print(f"SSL Error: {e}")
except httpx.HTTPError as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"Error: {e}")

# Test with requests
print(f"\n5. Testing connection to api.openai.com with requests:")
try:
    response = requests.get("https://api.openai.com/v1/models")
    print(f"Success! Status code: {response.status_code}")
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== End of Diagnostics ===") 